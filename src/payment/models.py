from decimal import Decimal

from auditlog.registry import auditlog
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from src.payment.enums import PaymentEnum
from src.payment.utils import get_creator_balance
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
    # These two are required for GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def amount_for_creator(self):
        amount = get_creator_balance(amount_in_coins=self.amount)
        return f'{amount} $'

    def amount_for_user(self):
        return f'{self.amount} coins'


class Balance(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def get_balance_as_number(self) -> Decimal | int:
        if self.user.is_creator():
            return self._creator_balance()

        return self._user_balance()

    def get_balance_as_string(self) -> str:
        if self.user.is_creator():
            return f'${self.get_balance_as_number()}'
        else:
            return f'{self.get_balance_as_number()} coins'

    def _creator_balance(self) -> Decimal:
        return get_creator_balance(amount_in_coins=self.balance)

    def _user_balance(self) -> Decimal:
        return self.balance


class Package(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    bonus = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()


auditlog.register(PaymentHistory)
auditlog.register(Balance)
