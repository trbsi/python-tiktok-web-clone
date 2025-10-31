from app import settings
from src.payment.enums import PaymentEnum
from src.payment.models import PaymentHistory
from src.payment.services.payment_providers.ccbill.ccbill_create_checkout_service import CcbillCreateCheckoutService
from src.payment.services.payment_providers.ccbill.ccbill_webhook_service import CCBillWebhookService
from src.payment.value_objects.checkout_value_object import CheckoutValueObject
from src.payment.value_objects.payment_webhook_value_object import PaymentWebhookValueObject


class PaymentProviderService():
    def __init__(
            self,
            ccbill_create_checkout_service: CcbillCreateCheckoutService | None = None,
            ccbill_webhook_service: CCBillWebhookService | None = None,
    ):
        self.default_payment_provider = settings.DEFAULT_PAYMENT_PROVIDER
        self.ccbill_create_checkout_service = ccbill_create_checkout_service
        self.ccbill_webhook_service = ccbill_webhook_service

    def create_checkout(self, payment_history: PaymentHistory) -> CheckoutValueObject:
        if self.default_payment_provider == PaymentEnum.PROVIDER_CCBILL.value:
            return self.ccbill_create_checkout_service.create_checkout(payment_history)

        raise Exception('Payment provider is not supported.')

    def handle_webook(self, body: dict) -> PaymentWebhookValueObject:
        if self.default_payment_provider == PaymentEnum.PROVIDER_CCBILL.value:
            return self.ccbill_webhook_service.handle_webhook(body)

        raise Exception('Payment provider is not supported.')
