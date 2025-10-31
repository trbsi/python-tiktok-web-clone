from src.payment.models import PaymentHistory
from src.payment.value_objects.checkout_value_object import CheckoutValueObject


class CcbillCreateCheckoutService:
    def create_checkout(self, payment_history: PaymentHistory) -> CheckoutValueObject:
        # some api call here
        user = payment_history.user
        apicall_result = object(user)
        apicall_result.id = 111
        apicall_result.url = 'https://payments.ccbill.com/callback/'

        payment_history.provider_payment_id = apicall_result.id
        payment_history.save()

        return CheckoutValueObject(apicall_result.url)
