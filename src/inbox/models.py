from django.db import models

from src.user.models import User as User


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_performer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

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
