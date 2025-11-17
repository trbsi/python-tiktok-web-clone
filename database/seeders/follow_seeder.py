from django.contrib.auth.models import Group

from src.follow.models import Follow
from src.user.enum import UserEnum


class FollowSeeder:
    @staticmethod
    def seed():
        user_group = Group.objects.get(name=UserEnum.ROLE_USER.value)
        users = user_group.user_set.all()

        creator_group = Group.objects.get(name=UserEnum.ROLE_CREATOR.value)
        creators = creator_group.user_set.all()

        for index, creator in enumerate(creators):
            if index % 2 == 0:
                pass

            for user in users:
                Follow.objects.create(follower=user, following=creator)
