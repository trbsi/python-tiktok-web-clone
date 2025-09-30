from src.media.enums import MediaEnum
from src.media.models import Media
from src.media.services.hashtag.hashtag_service import HashtagService
from src.user.models import User
from src.user.tasks import delete_user_media


class UpdateMyContentService:
    def update_my_content(self, user: User, delete_list: list, ids: list, descriptions: list):
        hashtag_service = HashtagService()
        Media.objects.filter(user=user).filter(id__in=delete_list).update(status=MediaEnum.STATUS_DELETED.value)

        for (index, id) in enumerate(ids):
            description = descriptions[index]
            media = Media.objects.filter(user=user, id=id).first()
            if media:
                media.description = description
                media.save()
                hashtag_service.save_hashtags(media=media, description=description)

        delete_user_media.delay(user_id=user.id)
