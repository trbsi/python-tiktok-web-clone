from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import QuerySet, OuterRef, Exists

from src.engagement.models import Like
from src.follower.models import Follow
from src.media.models import Media
from src.user.models import User


class LoadFeedService:
    PER_PAGE = 25

    def get_feed_items(self, page: int, user: User | AnonymousUser) -> list:
        per_page = self.PER_PAGE
        likes = Like.objects.none()
        following = Follow.objects.none()
        if user.is_authenticated:
            likes = Like.objects.filter(user=user, media=OuterRef('pk'))  # pk (primary key) from media table
            following = Follow.objects.filter(follower=user, following=OuterRef('user_id'))  # user_id from media table

        items: QuerySet[Media] = (
            Media.objects
            .order_by('-created_at')
            .annotate(liked=Exists(likes), followed=Exists(following))
        )

        paginator = Paginator(object_list=items, per_page=per_page)
        page = paginator.page(page)

        result = []
        for item in page.object_list:
            result.append({
                'id': item.id,
                'type': item.file_type,
                'src': item.get_file_url(),
                'like_count': item.like_count,
                'comments_count': item.comment_count,
                'description': item.description,
                'liked': item.liked,
                'followed': item.followed,
                'user': {
                    'username': item.user.username,
                    'avatar': item.user.get_avatar(),
                },
            })

        return result
