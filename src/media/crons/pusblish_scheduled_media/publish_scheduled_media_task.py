import zoneinfo
from datetime import timedelta, datetime

from django.db.models import Q
from django.utils import timezone

from src.media.enums import MediaEnum
from src.media.models import MediaScheduler, Media
from src.user.models import User, UserProfile


class PublishScheduledMediaTask:
    def publish_media(self):
        """
        Implements a round-robin content scheduler that automatically selects the next creator
        to post based on who has the oldest last_published_at timestamp,
        available scheduled media, and their local timezone posting window (morning, noon, or afternoon).
        Ensures fair rotation and timezone-aware publishing for all creators.
        """
        cutoff = timezone.now() - timedelta(hours=4)
        next_creator: MediaScheduler = (
            MediaScheduler.objects
            .filter(number_of_scheduled_media__gt=0)
            .filter(Q(last_published_at__isnull=True) | Q(last_published_at__lt=cutoff))
            .order_by('last_published_at')
            .first()
        )

        if not next_creator:
            return

        media: Media = (Media.objects
                        .filter(user=next_creator)
                        .filter(status=MediaEnum.STATUS_SCHEDULE.value)
                        .order_by('id')
                        .first())

        slot = self.get_local_time_window(next_creator)

        if not media and not slot:
            return

        media.status = MediaEnum.STATUS_PAID.value
        media.save()

        next_creator.last_published_at = timezone.now()
        next_creator.number_of_scheduled_media -= 1
        next_creator.save()

    def get_local_time_window(self, user: User) -> str | None:
        profile: UserProfile = user.profile
        timezone = zoneinfo.ZoneInfo(profile.timezone)
        local_now = datetime.now().astimezone(timezone)
        hour = local_now.hour

        if 8 <= hour < 12:
            return MediaScheduler.SLOT_MORNING
        elif 12 <= hour < 16:
            return MediaScheduler.SLOT_NOON
        elif 17 <= hour < 21:
            return MediaScheduler.SLOT_AFTERNOON
        return None
