from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from src.payment.services.my_payments.my_payments_service import MyPaymentsService


@require_GET
@login_required
def my_payments(request: HttpRequest) -> HttpResponse:
    get = request.GET
    page = int(get.get('page', 1))
    user = request.user

    service = MyPaymentsService()
    spendings = service.get_my_spendings(user=user, current_page=page)
    balance = service.get_balance(user=user)

    return render(
        request,
        'my_payments.html',
        {
            'spendings': spendings,
            'balance': balance,
            'user': user
        },
    )
