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


class Spending(models.Model):
    id = models.BigAutoField(primary_key=True)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spent_by_user')
    on_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spent_on_user')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    action_type = models.CharField(max_length=20)
    content_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def amount_for_creator(self):
        amount = round(self.amount / Balance.COIN_TO_FIAT, 2)
        return f'{amount} $'

    def amount_for_user(self):
        return f'{self.amount} coins'


class Balance(models.Model):
    COIN_TO_FIAT = 100  # 100 coins = 1$

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def get_balance_as_number(self) -> float | int:
        if self.user.is_creator():
            return self._creator_balance()

        return self._user_balance()

    def get_balance_as_string(self) -> str:
        if self.user.is_creator():
            suffix = '$'
        else:
            suffix = 'coins'

        return f'{self.get_balance_as_number()} {suffix}'

    def _creator_balance(self):
        return round(self.balance / self.COIN_TO_FIAT, 2)

    def _user_balance(self):
        return self.balance


auditlog.register(PaymentHistory)
auditlog.register(Balance)
