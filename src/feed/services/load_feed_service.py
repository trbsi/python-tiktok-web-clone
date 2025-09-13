from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import QuerySet, OuterRef, Exists

from src.engagement.models import Like
from src.follower.models import Follow
from src.media.models import Media
from src.user.models import User


class LoadFeedService:
    PER_PAGE = 25

    def get_following_feed(self, page: int, user: User | AnonymousUser) -> list:
        following_list = []
        if user.is_authenticated:
            following_list = Follow.get_following(user).values_list('id', flat=True)

        return self._get_feed_items(page=page, user=user, following_list=following_list)

    def get_discover_feed(self, page: int, user: User | AnonymousUser) -> list:
        return self._get_feed_items(page=page, user=user)

    def _get_feed_items(
            self,
            page: int,
            user: User | AnonymousUser,
            following_list: list = []
    ) -> list:
        likes = Like.objects.none()
        is_following = Follow.objects.none()

        if user.is_authenticated:
            # pk (primary key) from media table
            likes = Like.objects.filter(user=user, media=OuterRef('pk'))
            # user_id from media table
            is_following = Follow.objects.filter(follower=user, following=OuterRef('user_id'))

        items: QuerySet[Media] = (
            Media.objects
            .order_by('-created_at')
            .annotate(liked=Exists(likes), followed=Exists(is_following))
        )

        if following_list:
            items = items.filter(user__id__in=following_list)

        paginator = Paginator(object_list=items, per_page=self.PER_PAGE)
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
