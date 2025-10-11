from django.contrib.auth.models import Group

from src.core.utils import get_ip_data
from src.payment.models import Balance
from src.user.enum import UserEnum
from src.user.models import UserProfile, User


class PostRegistrationService:
    def post_register(self, user: User, ip: str | None) -> None:
        Balance.objects.create(user=user)

        role_user = Group.objects.get_or_create(name=UserEnum.ROLE_USER.value)
        role_user.user_set.add(user)

        ip_data = get_ip_data(ip)

        try:
            profile: UserProfile = user.profile
            profile.timezone = ip_data.timezone
            profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user, timezone=ip_data.timezone)
