import datetime

from django.db import transaction
from django.utils import timezone

from src.media.enums import MediaEnum
from src.media.models import Media, Unlock
from src.payment.services.spendings.spend_service import SpendService
from src.user.models import User


class UnlockService():
    def __init__(self, spend_service: SpendService | None = None):
        self.spend_service = spend_service or SpendService()

    @transaction.atomic
    def unlock(self, user: User, media_id: int) -> dict:
        media: Media = Media.objects.get(id=media_id)
        amount = self.spend_service.spend_media_unlock(user=user, media=media)
        Unlock.objects.create(
            user=user,
            media=media,
            expires_at=timezone.now() + datetime.timedelta(days=1),
            amount=amount,
            unlock_type=MediaEnum.UNLOCK_24H.value,
        )

        return {
            'media_id': media_id,
            'full_url': media.get_file_url()
        }
