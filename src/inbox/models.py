from django.db import models

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
    content = models.TextField()
    attachment_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
