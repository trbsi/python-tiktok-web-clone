from datetime import timedelta

from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

from app import settings
from src.user.enum import UserEnum
from src.user.query_managers import UserQueryManager


# instance: UserProfile
def profile_image_upload_path(user_profile, filename: str) -> str:
    return f'user_profile/{user_profile.user_id}/{filename}'


class User(AbstractUser):
    def __str__(self):
        return self.username

    objects = UserQueryManager()
    all_objects = models.Manager()

    def get_profile_picture(self):
        profile_image = str(self.profile.profile_image)
        if profile_image != '' and profile_image is not None:
            return settings.MEDIA_URL + profile_image

        return f"https://ui-avatars.com/api/?name={self.username}"

    def is_regular_user(self) -> bool:
        return self.groups.filter(name=UserEnum.ROLE_USER.value).exists()

    def is_creator(self) -> bool:
        return self.groups.filter(name=UserEnum.ROLE_CREATOR.value).exists()

    def get_role(self) -> str:
        return self.groups.first().name


class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to=profile_image_upload_path, null=True, blank=True)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    media_count = models.IntegerField(default=0)
    timezone = models.CharField(max_length=30, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    state_code = models.CharField(max_length=2, null=True, blank=True)

    objects = models.Manager()


class EmailChangeToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < now() - timedelta(hours=24)  # 24h validity


auditlog.register(User)
auditlog.register(UserProfile)
auditlog.register(EmailChangeToken)
