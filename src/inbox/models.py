from django.db import models

from src.user.models import User as User


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_sender')  # user
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_receiver')  # performer
    last_message = models.TextField(null=True)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('sender', 'receiver'), name='conversation_unique_sender_receiver')
        ]


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    content = models.TextField()
    attachment_url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
