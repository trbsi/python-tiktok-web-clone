from src.user.models import User


class UserProfileService:
    def get_user(self, username: str) -> User:
        return User.objects.filter(username=username).first()
