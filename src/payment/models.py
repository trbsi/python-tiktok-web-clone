from django.db import models

from src.payment.enums import PaymentEnum
from src.user.models import User


class PaymentHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    provider = models.CharField(max_length=10, choices=PaymentEnum.providers())
    provider_payment_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=PaymentEnum.statuses())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=10, choices=PaymentEnum.providers())
    provider_payment_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=PaymentEnum.statuses())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
