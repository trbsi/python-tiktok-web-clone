import zoneinfo
from datetime import datetime

from django.db.models import QuerySet, Count, F
from django.utils import timezone

from src.media.crons.publish_scheduled_media.scheduled_media_collection import ScheduledMediaCollection
from src.media.crons.publish_scheduled_media.scheduled_media_value_object import ScheduledMediaValueObject
from src.media.crons.schedule_slots_service import ScheduleSlotsService
from src.media.enums import MediaEnum
from src.media.models import MediaScheduler, Media


class PublishScheduledMediaCron:
    def publish_scheduled_media(self):
        """
        Implements a round-robin content scheduler that automatically selects the next creator
        to post based on who has the oldest last_published_at timestamp,
        available scheduled media, and their local timezone posting window (morning, afternoon or evening).
        Ensures fair rotation and timezone-aware publishing for all creators.

        Code calculates how many creators per minute it has to handle in order to cover all creators withing time slot.

        round-robin: a simple method for fairly distributing items or tasks in a rotating, sequential order, ensuring everyone in a group gets a turn before anyone gets a second one
        """

        # Get scheduled media grouped by timezone
        timezones_for_posting: QuerySet[MediaScheduler] = (
            MediaScheduler.objects
            .filter(number_of_scheduled_media__gt=0)
            .exclude(last_slot=F('current_slot'))
            .values('timezone')
            .annotate(user_count=Count('user'))
        )

        if not timezones_for_posting.exists():
            return

        # find all scheduled media who match post time in their timezone
        scheduled_media_collection = self._get_posting_slot_data(timezones_for_posting)
        if scheduled_media_collection.is_empty():
            return

        # find scheduled media by timezone so you can start publishing by timezone
        for scheduled_media in scheduled_media_collection.scheduled_media:
            per_page = scheduled_media.process_creators_per_minute_count()
            next_creators: QuerySet[MediaScheduler] = (
                MediaScheduler.objects
                .filter(number_of_scheduled_media__gt=0)
                .filter(timezone=scheduled_media.timezone)
                .order_by('last_published_at')[:per_page]
            )
            if not next_creators.exists():
                continue

            self._start_publishing(next_creators, scheduled_media)

    def _start_publishing(
            self,
            next_creators: QuerySet[MediaScheduler],
            schedule_creator: ScheduledMediaValueObject
    ) -> None:
        for next_creator in next_creators:
            media: Media = (
                Media.objects
                .filter(user=next_creator.user)
                .filter(status=MediaEnum.STATUS_SCHEDULE.value)
                .order_by('id')
                .first()
            )

            # Maybe user removed scheduled media but counter left intact
            if next_creator.number_of_scheduled_media > 0:
                next_creator.number_of_scheduled_media -= 1
                next_creator.save()

            if media:
                media.status = MediaEnum.STATUS_PAID.value
                media.save()

                next_creator.last_published_at = timezone.now()
                next_creator.last_slot = schedule_creator.current_slot_name
                next_creator.save()

    def _get_posting_slot_data(self, timezones_for_posting: QuerySet[MediaScheduler]) -> ScheduledMediaCollection:
        """
        Prepare data grouped by timezone so you can calculate which media should be posted and how many of them per minute
        """
        result = []
        for media_scheduler in timezones_for_posting:
            tz = zoneinfo.ZoneInfo(media_scheduler['timezone'])
            now = datetime.now(tz)
            local_time = now.time()

            start, end, slot_name = ScheduleSlotsService.get_current_slot(local_time)
            if slot_name:
                end_dt = datetime.combine(now.date(), end, tz)
                minutes_left = int((end_dt - now).total_seconds() / 60)
                result.append(ScheduledMediaValueObject(
                    minutes_left=minutes_left,
                    current_slot_name=slot_name,
                    number_of_creators=media_scheduler['user_count'],
                    timezone=media_scheduler['timezone']
                ))

        return ScheduledMediaCollection(*result)
