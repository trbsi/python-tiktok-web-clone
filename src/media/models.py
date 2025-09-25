from auditlog.registry import auditlog
from django.db import models

from app import settings
from src.media.enums import MediaEnum
from src.media.query_managers import MediaManager
from src.user.models import User as User


class Media(models.Model):
    def get_upload_to_path(self, media, filename: str):
        return f'user_profile/{media.user_id}/{filename}'

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_user')
    file_info = models.JSONField()
    file_thumbnail = models.JSONField(null=True, blank=True)
    file_trailer = models.JSONField(null=True, blank=True)
    file_type = models.CharField(max_length=20, choices=MediaEnum.file_types())
    status = models.CharField(max_length=20, choices=MediaEnum.statuses())
    description = models.TextField(null=True)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MediaManager()
    all_objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['status'], name='idx_media_status'),
        ]

    def get_file_url(self):
        return f'{settings.STORAGE_CDN_URL}/{self.file_info.get('file_name')}'

    def get_thumbnail_url(self):
        return f'{settings.STORAGE_CDN_URL}/{self.file_thumbnail.get('file_name')}'

    def is_image(self):
        return self.file_type == MediaEnum.FILE_TYPE_IMAGE.value

    def is_video(self):
        return self.file_type == MediaEnum.FILE_TYPE_VIDEO.value


auditlog.register(Media)
