from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from src.payment.models import Balance, Package
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


# no need for @login_required here
@require_GET
def api_get_balance(request: HttpRequest) -> JsonResponse:
    user: User | AnonymousUser = request.user
    if user.is_anonymous:
        return JsonResponse({'balance': None, 'status': 'not_authenticated'})

    balance: Balance = Balance.objects.get(user=user)
    balance.balance = 3
    status = 'ok'
    if balance.balance < 100:
        status = 'low_balance'

    return JsonResponse({'balance': balance.balance, 'status': status})


@require_GET
@login_required
def buy_packages(request: HttpRequest) -> HttpResponse:
    context = {
        'packages': Package.objects.all(),
    }
    return render(request, 'buy_packages.html', context)
