from django.contrib.auth.models import User
from django.db import models


class Media(models.Model):
    STATUS_PUBLIC = 'public'
    STATUS_PENDING = 'pending'
    STATUS_LOCKED = 'locked'
    STATUS_PRIVATE = 'private'

    FILE_TYPE_AUDIO = 'audio'
    FILE_TYPE_VIDEO = 'video'
    FILE_TYPE_IMAGE = 'image'

    STATUSES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('pending', 'Pending'),
        ('locked', 'Locked'),
    )
    FILE_TYPE = (
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('image', 'Image'),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    file = models.FileField(upload_to='uploads/videos')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE)
    status = models.CharField(max_length=20, choices=STATUSES)
    description = models.TextField(null=True)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        return self.file
