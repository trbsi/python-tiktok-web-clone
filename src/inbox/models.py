from django.db import models

from src.inbox.enums import InboxEnum
from src.inbox.query_managers import InboxQueryManager
from src.user.models import User as User


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_performer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_user')
    status = models.CharField(max_length=10, choices=InboxEnum.statuses(), default=InboxEnum.STATUS_ACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = InboxQueryManager()
    all_objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('performer', 'user'), name='conversation_unique_performer_user')
        ]


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    content = models.TextField()
    attachment_url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
