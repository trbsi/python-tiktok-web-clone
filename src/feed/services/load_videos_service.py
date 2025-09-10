from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import QuerySet, OuterRef, Exists

from src.engagement.models import Like
from src.media.models import Media
from src.user.models import User


class LoadVideosService:
    def __init__(self, per_page: int, page: int):
        self.per_page = per_page
        self.page = page

    def get_videos(self, user: AnonymousUser | User) -> list:
        likes = []
        if user.is_authenticated:
            likes = Like.objects.filter(user=user, media=OuterRef('pk'))

        items: QuerySet[Media] = (Media.objects
                                  .filter(status=Media.STATUS_PUBLIC)
                                  .annotate(liked=Exists(likes)))

        paginator = Paginator(object_list=items, per_page=self.per_page)
        page = paginator.page(self.page)

        result = []
        for item in page.object_list:
            avatar = str(item.user.profile.profile_image) if (
                item.user.profile.profile_image) else f"https://ui-avatars.com/api/?name={item.user.username}"
            result.append({
                'id': item.id,
                'likes': item.like_count,
                'comments_count': item.comment_count,
                'description': item.description,
                'liked': item.liked,
                'user': {
                    'username': item.user.username,
                    'avatar': avatar,
                },
            })

        return result
