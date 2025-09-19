from django.db import models

from src.media.enums import MediaEnum
from src.media.query_managers import MediaManager
from src.user.models import User as User


class Media(models.Model):

    def get_upload_to_path(self, media, filename: str):
        return f'user_profile/{media.user_id}/{filename}'

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_user')
    file = models.FileField(upload_to='uploads/media', max_length=255)
    file_thumbnail = models.FileField(upload_to='uploads/media', max_length=255, null=True)
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
        return str(self.file)

    def get_thumbnail_url(self):
        return str(self.file_thumbnail)
