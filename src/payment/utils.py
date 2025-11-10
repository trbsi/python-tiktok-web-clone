# creator balance deducted by platform fee
from decimal import Decimal

from src.payment.enums import PaymentEnum
from src.payment.value_objects.user_balance_value_object import UserBalanceValueObject


def get_creator_balance_in_fiat(coins: Decimal) -> UserBalanceValueObject:
    return UserBalanceValueObject(coins)


def coin_to_fiat(amount_in_coins: Decimal) -> Decimal:
    coin_to_fiat = Decimal(PaymentEnum.COIN_TO_FIAT.value)
    return amount_in_coins / coin_to_fiat
