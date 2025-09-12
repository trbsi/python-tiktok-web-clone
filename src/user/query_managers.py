from django.contrib.auth.models import UserManager
from django.db import models


class UserQueryManager(UserManager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True)
