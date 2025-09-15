from django.contrib.auth.models import AbstractUser
from django.db import models

from app import settings
from src.user.enum import UserEnum
from src.user.query_managers import UserQueryManager


class User(AbstractUser):
    def __str__(self):
        return self.username

    objects = UserQueryManager()
    all_objects = models.Manager()

    def get_avatar(self):
        if self.profile.profile_image != '':
            return str(self.profile.profile_image)

        return f"https://ui-avatars.com/api/?name={self.username}"

    def is_regular_user(self) -> bool:
        return self.groups.filter(name=UserEnum.ROLE_USER.value).exists()


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True)
    profile_image = models.ImageField(upload_to='uploads/profile_image', null=True)
