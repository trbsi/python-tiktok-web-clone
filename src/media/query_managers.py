from django.db import models

from src.media.enums import MediaEnum


class MediaManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=MediaEnum.STATUS_FREE.value)
