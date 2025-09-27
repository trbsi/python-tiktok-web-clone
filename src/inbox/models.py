from auditlog.registry import auditlog
from django.db import models

from app import settings
from src.media.enums import MediaEnum
from src.user.models import User as User


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_recipient')
    last_message = models.TextField(null=True)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_recipient = models.BooleanField(default=False)
    read_by_sender = models.BooleanField(default=False)
    read_by_recipient = models.BooleanField(default=False)
    is_automated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('sender', 'recipient'), name='conversation_unique_sender_recipient')
        ]

    def get_other_user(self, current_user: User) -> User:
        if current_user == self.sender:
            return self.recipient
        return self.sender

    def is_read(self, current_user: User) -> bool:
        if current_user == self.sender:
            return self.read_by_sender

        return self.read_by_recipient


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    message = models.TextField(null=True)
    file_info = models.JSONField(null=True)
    file_type = models.CharField(max_length=10, null=True, choices=MediaEnum.file_types())
    is_automated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def get_attachment_url(self) -> str | None:
        if self.file_info is None:
            return None

        return f'{settings.STORAGE_CDN_URL}/{self.file_info.get('file_name')}'

    def is_image(self):
        return self.file_type == MediaEnum.FILE_TYPE_IMAGE.value

    def is_video(self):
        return self.file_type == MediaEnum.FILE_TYPE_VIDEO.value


auditlog.register(Conversation)
auditlog.register(Message)
