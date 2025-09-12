from django.db import models

from src.inbox.enums import InboxEnum


class InboxQueryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=InboxEnum.STATUS_ACTIVE.value)
