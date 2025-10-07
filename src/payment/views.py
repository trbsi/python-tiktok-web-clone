from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from src.payment.models import Balance
from src.payment.services.my_payments.my_payments_service import MyPaymentsService
from src.user.models import User


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


@require_GET
@login_required
def api_get_balance(request: HttpRequest) -> JsonResponse:
    user: User | AnonymousUser = request.user
    if user.is_anonymous:
        return JsonResponse({"balance": None})

    balance: Balance = Balance.objects.get(user=user)

    return JsonResponse({"balance": balance.balance})
