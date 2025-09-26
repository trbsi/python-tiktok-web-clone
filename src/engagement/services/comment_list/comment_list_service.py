from typing import List

from django.db.models import QuerySet

from app import settings
from src.engagement.models import Comment


class CommentListService():
    def list(self, media_id) -> List:
        comments: QuerySet[Comment] = Comment.objects.filter(media_id=media_id).order_by('-created_at')

        result = []
        for comment in comments:
            result.append({
                'id': comment.id,
                'text': comment.comment,
                'created_at': comment.created_at.strftime(settings.DATE_TIME_FORMAT),
                'user': {
                    'username': comment.user.username,
                    'avatar': comment.user.get_profile_picture(),
                }
            })

        return result
