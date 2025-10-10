from django.contrib.auth.models import Group

from src.core.utils import get_timezone_from_ip
from src.payment.models import Balance
from src.user.enum import UserEnum
from src.user.models import UserProfile, User


class PostRegistrationService:
    def post_register(self, user: User, ip: str | None) -> None:
        Balance.objects.create(user=user)

        role_user = Group.objects.get_or_create(name=UserEnum.ROLE_USER.value)
        role_user.user_set.add(user)

        timezone = get_timezone_from_ip(ip)
        try:
            profile = user.profile
            profile.timezone = timezone
            profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user, timezone=timezone)
