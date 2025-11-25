from decimal import Decimal

from django.db import transaction

from src.media.enums import MediaEnum
from src.media.models import Media
from src.media.services.hashtag.hashtag_service import HashtagService
from src.media.utils import replace_tags
from src.payment.utils import fiat_to_coins
from src.user.models import User, UserProfile
from src.user.tasks import task_delete_user_media


class UpdateMyContentService:
    def __init__(self, hashtag_service=None):
        self.hashtag_service = hashtag_service or HashtagService()

    def update_my_content(
            self,
            user: User,
            delete_list: list,
            ids: list,
            descriptions: list,
            unlock_prices: list,
            submit_type: str
    ):
        if submit_type == 'delete':
            Media.objects.filter(user=user).filter(id__in=delete_list).update(status=MediaEnum.STATUS_DELETED.value)
            profile: UserProfile = user.profile
            profile.media_count = profile.media_count - len(delete_list)
            profile.save()

        if submit_type == 'save':
            for (index, id) in enumerate(ids):
                description = replace_tags(descriptions[index])
                unlock_price = Decimal(unlock_prices[index])
                media: Media = Media.objects.filter(user=user, id=id).first()
                if media:
                    media.description = description
                    media.unlock_price = fiat_to_coins(unlock_price)
                    media.save()
                    self.hashtag_service.save_hashtags(media=media, description=description)

        transaction.on_commit(lambda: task_delete_user_media.delay(user_id=user.id))
