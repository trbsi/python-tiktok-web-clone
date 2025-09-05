from django.contrib.auth.models import User
from django.db import models


class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user1', 'user2'), name='conversation_unique_user')
        ]


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    content = models.TextField()
    attachment_url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
