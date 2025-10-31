from datetime import timedelta

from django.utils import timezone

from src.media.enums import MediaEnum
from src.media.models import Unlock


class LockMediaTask:
    def lock_media(self):
        yesterday = timezone.now() - timedelta(days=1)
        (Unlock.objects
         .filter(unlock_type=MediaEnum.UNLOCK_24H.value)
         .filter(unlocked_at__lte=yesterday)
         .delete())
