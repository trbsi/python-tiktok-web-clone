from src.media.models import Unlock
from src.user.models import User


class UnlockedMediaService():
    def get_unlocked_media(self, user: User, media_ids: list) -> set:
        if user.is_anonymous:
            return set()

        result = (
            Unlock.objects
            .filter(user=user, media_id__in=list(media_ids))
            .all()
            .values_list('media_id', flat=True)
        )

        return set(result)
