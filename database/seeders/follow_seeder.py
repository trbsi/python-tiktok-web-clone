from django.contrib.auth.models import Group

from src.follow.models import Follow
from src.user.enum import UserEnum


class FollowSeeder:
    @staticmethod
    def seed():
        user_group = Group.objects.get(name=UserEnum.ROLE_USER.value)
        users = user_group.user_set.all()

        performer_group = Group.objects.get(name=UserEnum.ROLE_PERFORMER.value)
        performers = performer_group.user_set.all()

        for index, performer in enumerate(performers):
            if index % 2 == 0:
                pass

            for user in users:
                Follow.objects.create(follower=user, following=performer)
