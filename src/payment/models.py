from auditlog.registry import auditlog
from django.db import models

from src.payment.enums import PaymentEnum
from src.user.models import User


class PaymentHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    provider = models.CharField(max_length=10, choices=PaymentEnum.providers())
    provider_payment_id = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=PaymentEnum.statuses())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()


class Balance(models.Model):
    COIN_TO_FIAT = 100  # 100 coins = 1$

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def performer_balance(self):
        return self.balance / self.COIN_TO_FIAT

    def user_balance(self):
        return self.balance


auditlog.register(PaymentHistory)
auditlog.register(Balance)
