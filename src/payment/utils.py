# creator balance deducted by platform fee
from decimal import Decimal, ROUND_HALF_UP

from src.payment.enums import PaymentEnum


def get_creator_balance(amount_in_coins: Decimal) -> Decimal:
    coin_to_fiat = Decimal(PaymentEnum.COIN_TO_FIAT.value)
    platform_commission = Decimal(PaymentEnum.COMMISSION_PERCENTAGE.value)

    balance_in_fiat: Decimal = amount_in_coins / Decimal(coin_to_fiat)
    commission: Decimal = balance_in_fiat * Decimal(platform_commission)
    final: Decimal = balance_in_fiat - commission

    return final.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
