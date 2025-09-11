from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import QuerySet, OuterRef, Exists

from src.engagement.models import Like
from src.follower.models import Follow
from src.media.models import Media
from src.user.models import User


class LoadFeedService:
    def get_feed_items(self, per_page: int, page: int, user: User | AnonymousUser) -> list:
        likes = Like.objects.none()
        following = Follow.objects.none()
        if user.is_authenticated:
            likes = Like.objects.filter(user=user, media=OuterRef('pk'))
            following = Follow.get_following(user=user)

        items: QuerySet[Media] = (Media.objects
                                  .order_by('-created_at')
                                  .annotate(liked=Exists(likes))
                                  .annotate(followed=Exists(following)))

        paginator = Paginator(object_list=items, per_page=per_page)
        page = paginator.page(page)

        result = []
        for item in page.object_list:
            avatar = str(item.user.profile.profile_image) if (
                item.user.profile.profile_image) else f"https://ui-avatars.com/api/?name={item.user.username}"
            result.append({
                'id': item.id,
                'src': item.get_file_url(),
                'like_count': item.like_count,
                'comments_count': item.comment_count,
                'description': item.description,
                'liked': item.liked,
                'followed': item.followed,
                'user': {
                    'username': item.user.username,
                    'avatar': avatar,
                },
            })

        return result
