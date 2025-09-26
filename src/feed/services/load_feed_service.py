from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import QuerySet, OuterRef, Exists, Case, Value, When, IntegerField

from src.engagement.models import Like
from src.follow.models import Follow
from src.media.models import Media
from src.user.models import User


class LoadFeedService:
    PER_PAGE = 25

    def get_following_feed(self, page: int, user: User | AnonymousUser, filters: str | None) -> dict:
        include_following_list = self._get_followings(user=user)
        return self._get_feed_items(
            current_page=page,
            user=user,
            include_following_list=include_following_list,
            filters=filters
        )

    def get_discover_feed(self, page: int, user: User | AnonymousUser) -> dict:
        exclude_following_list = self._get_followings(user=user)
        return self._get_feed_items(current_page=page, user=user, exclude_following_list=exclude_following_list)

    def _get_followings(self, user: User | AnonymousUser) -> list | None:
        if user.is_authenticated:
            return Follow.get_following(user).values_list('id', flat=True)

        return None

    def _get_feed_items(
            self,
            current_page: int,
            user: User | AnonymousUser,
            include_following_list: list | None = None,
            exclude_following_list: list | None = None,
            filters: str | None = None,
    ) -> dict:
        likes = Like.objects.none()
        is_following = Follow.objects.none()

        if user.is_authenticated:
            # pk (primary key) from media table
            likes = Like.objects.filter(user=user, media=OuterRef('pk'))
            # user_id from media table
            is_following = Follow.objects.filter(follower=user, following=OuterRef('user_id'))

        items: QuerySet[Media] = (
            Media.objects
            .select_related('user')
            .order_by('-created_at')
            .annotate(liked=Exists(likes), followed=Exists(is_following))
        )

        if include_following_list:
            items = items.filter(user_id__in=include_following_list)

        if exclude_following_list:
            items = items.exclude(user_id__in=exclude_following_list)

        # filters: uid,12,mid,55 -> comma separated
        if filters is not None:
            filters = filters.split(',')
            for index, value in enumerate(filters):
                if value == 'uid':
                    items = items.filter(user_id=filters[index + 1])
                elif value == 'mid':
                    items = items.annotate(is_target_media=Case(
                        When(id=filters[index + 1], then=Value(0)),
                        default=Value(1),
                        output_field=IntegerField()
                    )).order_by('is_target_media')

        paginator = Paginator(object_list=items, per_page=self.PER_PAGE)
        page = paginator.page(current_page)

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
                    'id': item.user.id,
                    'username': item.user.username,
                    'avatar': item.user.get_profile_picture(),
                },
            })

        next_page = page.next_page_number() if page.has_next() else None

        return {'result': result, 'next_page': next_page}
