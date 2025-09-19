from src.payment.models import Balance
from src.user.models import UserProfile


class PostRegistrationService:
    def register(self, user) -> None:
        Balance.objects.create(user=user)

        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user)
