from django.db.models import QuerySet

from src.media.models import Media
from src.user.models import User


class UserProfileService:
    def get_user(self, username: str) -> User:
        return User.objects.filter(username=username).first()

    def get_content(self, user: User) -> QuerySet[Media]:
        return Media.objects.filter(user=user).order_by('-created_at')
