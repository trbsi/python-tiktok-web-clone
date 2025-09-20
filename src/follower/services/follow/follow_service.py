from django.contrib.auth.models import AnonymousUser

from src.follower.models import Follow
from src.user.models import User


class FollowService:
    def follow(self, follower: User | AnonymousUser, user_id: int) -> None:
        if not follower.is_authenticated:
            return

        user_to_follow = User.objects.get(id=user_id)
        isFollowing: bool = Follow.is_following(user_a=follower, user_b=user_to_follow)

        if isFollowing:
            Follow.objects.filter(follower=follower, following=user_to_follow).api_delete()
        else:
            Follow.objects.create(follower=follower, following=user_to_follow)
