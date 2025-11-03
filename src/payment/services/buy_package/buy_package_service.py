import random

from app import settings
from src.payment.enums import PaymentEnum
from src.payment.models import PaymentHistory, Package
from src.payment.services.payment_providers.payment_provider_service import PaymentProviderService
from src.payment.services.payment_webhook.payment_webhook_service import PaymentWebhookService
from src.payment.value_objects.checkout_value_object import CheckoutValueObject
from src.user.models import User


class BuyPackageService():
    def __init__(self, provider_service: PaymentProviderService | None = None):
        self.payment_provider_service = provider_service or PaymentProviderService()

    def buy_package(self, user: User, package_id) -> str:
        package = Package.objects.get(id=package_id)

        # @TODO remove this variable
        random_int = random.randint(1, 10000)
        random_int = f'default_no_id_{random_int}'

        payment_history = PaymentHistory.objects.create(
            user=user,
            price=package.price,
            amount=package.amount,
            provider=settings.DEFAULT_PAYMENT_PROVIDER,
            provider_payment_id=random_int,
            status=PaymentEnum.STATUS_PENDING.value,
        )

        value_object: CheckoutValueObject = self.payment_provider_service.create_checkout(payment_history)
        payment_history.provider_payment_id = value_object.provider_payment_id
        payment_history.save()

        # @TODO remove payment_webhook call, this is just for debug
        PaymentWebhookService().handle_webook({
            'X-paymentid': random_int,
            'eventType': 'NewSaleSuccess',
        })

        return value_object.redirect_url
