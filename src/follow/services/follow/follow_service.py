from django.contrib.auth.models import AnonymousUser

from src.follow.models import Follow
from src.user.models import User


class FollowService:
    def follow_unfollow(self, follower: User | AnonymousUser, following: int) -> str:
        if not follower.is_authenticated:
            return ''

        is_following: bool = Follow.is_following(user_a=follower.id, user_b=following)

        user_to_follow = User.objects.get(id=following)
        if is_following:
            Follow.objects.filter(follower=follower, following=user_to_follow).delete()
            return 'unfollowed'
        else:
            Follow.objects.create(follower=follower, following=user_to_follow)
            return 'followed'
