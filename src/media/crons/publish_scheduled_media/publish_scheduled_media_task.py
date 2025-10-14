import zoneinfo
from datetime import datetime, time

from django.db.models import QuerySet, Count, F
from django.utils import timezone

from src.media.crons.publish_scheduled_media.schedule_creator_collection import ScheduleCreatorCollection
from src.media.crons.publish_scheduled_media.schedule_creator_value_object import ScheduleCreatorValueObject
from src.media.enums import MediaEnum
from src.media.models import MediaScheduler, Media


class PublishScheduledMediaTask:
    # Define posting slots as (start_hour, end_hour)
    SLOTS = [
        (time(8, 0), time(10, 0), MediaScheduler.SLOT_MORNING),  # Morning: 8–10
        (time(14, 0), time(16, 0), MediaScheduler.SLOT_AFTERNOON),  # Afternoon: 14–16
        (time(18, 0), time(20, 0), MediaScheduler.SLOT_EVENING),  # Evening: 18–20
    ]

    def publish_media(self):
        """
        Implements a round-robin content scheduler that automatically selects the next creator
        to post based on who has the oldest last_published_at timestamp,
        available scheduled media, and their local timezone posting window (morning, noon, or afternoon).
        Ensures fair rotation and timezone-aware publishing for all creators.
        """

        # Grouped by timezone
        timezones_for_posting: QuerySet[MediaScheduler] = (
            MediaScheduler.objects
            .filter(number_of_scheduled_media__gt=0)
            .exclude(last_slot=F('next_slot'))
            .values('timezone')
            .annotate(user_count=Count('user'))
        )

        if not timezones_for_posting.exists():
            return

        # find all creators who match post time in their timezone
        schedule_creator_collection = self._get_posting_slot_data(timezones_for_posting)
        if schedule_creator_collection.is_empty():
            return

        # find by timezone so you can start publishing by timezone
        for schedule_creator in schedule_creator_collection.schedule_creator:
            per_page = schedule_creator.process_creators_per_minute_count()
            next_creators: QuerySet[MediaScheduler] = (
                MediaScheduler.objects
                .filter(number_of_scheduled_media__gt=0)
                .filter(timezone=timezone)
                .exclude(last_slot=schedule_creator.current_slot_name)
                .order_by('last_published_at')[:per_page]
            )
            if not next_creators.exists():
                continue

            self._start_publishing(next_creators, schedule_creator)

    def _start_publishing(
            self,
            next_creators: QuerySet[MediaScheduler],
            schedule_creator: ScheduleCreatorValueObject
    ) -> None:
        for next_creator in next_creators:
            media: Media = (
                Media.objects
                .filter(user=next_creator.user)
                .filter(status=MediaEnum.STATUS_SCHEDULE.value)
                .order_by('id')
                .first()
            )

            if not media:
                continue

            media.status = MediaEnum.STATUS_PAID.value
            media.save()

            next_creator.last_published_at = timezone.now()
            next_creator.number_of_scheduled_media -= 1
            next_creator.last_slot = schedule_creator.current_slot_name
            next_creator.save()

    def _get_posting_slot_data(self, timezones_for_posting: QuerySet[MediaScheduler]) -> ScheduleCreatorCollection:
        """
        Prepare data grouped by timezone so you can calculate which creators should be posted and how many of them per minute
        """
        result = []
        for media_scheduler in timezones_for_posting:
            tz = zoneinfo.ZoneInfo(media_scheduler.timezone)
            now = datetime.now(tz)
            local_time = now.time()

            for start, end, slot_name in self.SLOTS:
                if start <= local_time < end:
                    end_dt = datetime.combine(now.date(), end, tz)
                    minutes_left = int((end_dt - now).total_seconds() / 60)
                    result.append(ScheduleCreatorValueObject(
                        timezone=media_scheduler.timezone,
                        minutes_left=minutes_left,
                        current_slot_name=slot_name,
                        number_of_creators=media_scheduler.user_count
                    ))
                    break

        return ScheduleCreatorCollection(*result)
