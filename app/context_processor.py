import os

from django.urls import reverse_lazy

from src.user.models import User


def environment_variables(request):
    user: User = request.user
    is_authenticated = user.is_authenticated
    is_creator = False
    if is_authenticated:
        is_creator = user.is_creator()

    return {
        'TEMPLATE_APP_NAME': os.getenv('APP_NAME'),
        'TEMPLATE_SUPPORT_EMAIL': os.getenv('SUPPORT_EMAIL'),
        'TEMPLATE_BAlANCE_ENDPOINT': reverse_lazy('payment.api.get_balance'),
        'TEMPLATE_IS_AUTHENTICATED': is_authenticated,
        'TEMPLATE_IS_CREATOR': is_creator
    }
