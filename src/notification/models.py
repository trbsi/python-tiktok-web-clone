from django.db import models

from src.user.models import User


class WebPushSubscription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.JSONField()

    objects = models.Manager()
