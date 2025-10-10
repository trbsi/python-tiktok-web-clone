from django.contrib.auth.models import Group

from src.payment.models import Balance
from src.user.enum import UserEnum
from src.user.models import UserProfile


class PostRegistrationService:
    def post_register(self, user) -> None:
        Balance.objects.create(user=user)
        role_user = Group.objects.get_or_create(name=UserEnum.ROLE_USER.value)
        role_user.user_set.add(user)

        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user)
