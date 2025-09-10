from django.db import models

from src.user.models import User

PROVIDER_SEGPAY = 'segpay'
PROVIDER_EPOCH = 'epoch'
PROVIDERS = (
    (PROVIDER_SEGPAY, 'segpay'),
    (PROVIDER_EPOCH, 'epoch'),
)

STATUS_PENDING = 'pending'
STATUS_APPROVED = 'approved'
STATUS_CANCELED = 'canceled'
STATUS_CHOICES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_APPROVED, 'Approved'),
    (STATUS_CANCELED, 'Canceled'),
)


class PaymentHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    provider = models.CharField(max_length=10, choices=PROVIDERS)
    provider_payment_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=10, choices=PROVIDERS)
    provider_payment_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
