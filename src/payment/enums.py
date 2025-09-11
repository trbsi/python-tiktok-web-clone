from enum import Enum
from typing import Tuple


class PaymentEnum(Enum):
    PROVIDER_SEGPAY = 'segpay'
    PROVIDER_EPOCH = 'epoch'

    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_CANCELED = 'canceled'

    @staticmethod
    def statuses() -> Tuple:
        return (
            (PaymentEnum.STATUS_PENDING.value, 'Pending'),
            (PaymentEnum.STATUS_APPROVED.value, 'Approved'),
            (PaymentEnum.STATUS_CANCELED.value, 'Canceled'),
        )

    @staticmethod
    def providers() -> Tuple:
        return (
            (PaymentEnum.PROVIDER_SEGPAY.value, 'SegGay'),
            (PaymentEnum.PROVIDER_EPOCH.value, 'Epoch'),
        )
