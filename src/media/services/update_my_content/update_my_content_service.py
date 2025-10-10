from src.media.enums import MediaEnum
from src.media.models import Media
from src.media.services.hashtag.hashtag_service import HashtagService
from src.user.models import User, UserProfile
from src.user.tasks import delete_user_media


class UpdateMyContentService:
    def __init__(self, hashtag_service=None):
        self.hashtag_service = hashtag_service or HashtagService()

    def update_my_content(
            self,
            user: User,
            delete_list: list,
            ids: list,
            descriptions: list,
            statuses: list
    ):
        if delete_list:
            Media.objects.filter(user=user).filter(id__in=delete_list).update(status=MediaEnum.STATUS_DELETED.value)
            profile:UserProfile = user.profile
            profile.media_count = profile.media_count - len(delete_list)
            profile.save()
            return

        for (index, id) in enumerate(ids):
            description = descriptions[index]
            status = statuses[index]
            media = Media.objects.filter(user=user, id=id).first()
            if media:
                media.description = description
                media.status = status
                media.save()
                self.hashtag_service.save_hashtags(media=media, description=description)

        delete_user_media.delay(user_id=user.id)
