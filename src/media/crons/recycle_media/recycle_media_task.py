import random
from datetime import timedelta

from django.utils import timezone

from src.media.models import MediaScheduler, Media


class RecycleMediaTask:
    def recycle_media(self):
        """
        Find a media that was not published for at least a day
        If current_slot is not null it means that media is read to be published
        Slots are scheduled via UpdateCreatorTimezoneSlotsTask
        """
        past_date = timezone.now() - timedelta(days=1)
        creators_not_published_for_a_while = (
            MediaScheduler.objects
            .filter(number_of_scheduled_media=0)
            .filter(last_published_at__lte=past_date)
            .filter(current_slot__isnull=False)
            .order_by('last_published_at')[:100]
        )

        for media_scheduler in creators_not_published_for_a_while:
            user_media = Media.objects.filter(user=media_scheduler.user).order_by('id')
            user_media_count = user_media.count()
            if user_media_count == 0:
                continue
            random_index = random.randint(0, user_media_count - 1)
            result = user_media[random_index]
