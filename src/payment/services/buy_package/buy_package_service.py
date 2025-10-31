from app import settings
from src.payment.enums import PaymentEnum
from src.payment.models import PaymentHistory, Package, Balance
from src.payment.services.payment_providers.payment_provider_service import PaymentProviderService
from src.user.models import User


class BuyPackageService():
    def __init__(self, provider_service: PaymentProviderService | None = None):
        self.payment_provider_service = provider_service or PaymentProviderService()

    def buy_package(self, user: User, package_id) -> str:
        package = Package.objects.get(id=package_id)

        payment_history = PaymentHistory.objects.create(
            user=user,
            amount=package.amount,
            provider=settings.DEFAULT_PAYMENT_PROVIDER,
            provider_payment_id='default_no_id',
            status=PaymentEnum.STATUS_PENDING.value,
        )

        # @TODO remove payment_webhook call, this is just for debug
        self.payment_webhook(user, {})

        checkout_value_object = self.payment_provider_service.create_checkout(payment_history)
        return checkout_value_object.redirect_url

    # @TODO finish webhook
    def payment_webhook(self, user: User, body: dict):
        self.payment_provider_service.handle_webook(body)
        payment_history = PaymentHistory.objects.get(user=user, provider_payment_id='default_no_id')
        payment_history.status = PaymentEnum.STATUS_APPROVED.value
        payment_history.save()

        balance = Balance.objects.get(user=user)
        balance.amount += payment_history.amount
        balance.save()
