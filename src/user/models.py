from django.contrib.auth.models import AbstractUser
from django.db import models

from app import settings


class User(AbstractUser):
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True)
    profile_image = models.ImageField(upload_to='uploads/profile_image', null=True)
