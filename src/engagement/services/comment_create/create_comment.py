from django.contrib.auth.models import AnonymousUser

from src.engagement.models import Comment
from src.media.models import Media
from src.user.models import User


class CreateComment():
    def create_comment(self, user: AnonymousUser | User, comment: str, media_id: int) -> dict:
        if user.is_authenticated == False:
            raise Exception("You are not authenticated")

        media = Media.objects.get(id=media_id)
        comment = Comment.objects.create(user=user, media=media, comment=comment)

        return {
            'id': comment.id,
            'text': comment.comment,
            'created_at': comment.created_at.strftime("%m/%d/%Y %H:%M:%S"),
            'user': {
                'username': comment.user.username,
                'avatar': comment.user.get_avatar(),
            }
        }
