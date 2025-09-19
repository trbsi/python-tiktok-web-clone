import random
import string

from src.engagement.models import Comment
from src.inbox.models import Conversation
from src.media.enums import MediaEnum
from src.media.models import Media
from src.user.models import User, UserProfile


class DeleteUserService:
    def delete(self, user: User) -> None:
        length = 10
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # TODO remove media from storage
        Media.objects.filter(user=user).update(status=MediaEnum.STATUS_DELETED.value)
        Comment.objects.filter(user=user).delete()
        Conversation.objects.filter(user=user).delete()

        user.username = f"{user.id}_deleted_user"
        user.first_name = f"{user.id}_deleted_user"
        user.last_name = f"{user.id}_deleted_user"
        user.email = f"{user.id}_deleted_user@deleted.xxx"
        user.is_active = False
        user.set_password(random_string)
        user.save()

        profile: UserProfile = user.profile
        profile.profile_image = None
        profile.bio = None
        profile.save()
