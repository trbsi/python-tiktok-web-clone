import os

from django.urls import reverse_lazy


def environment_variables(request):
    return {
        'APP_NAME': os.getenv('APP_NAME'),
        'SUPPORT_EMAIL': os.getenv('SUPPORT_EMAIL'),
        'BAlANCE_ENDPOINT': reverse_lazy('payment.api.get_balance')
    }
