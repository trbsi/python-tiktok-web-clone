import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from app.log import log
from src.payment.models import Balance, Package
from src.payment.services.buy_package.buy_package_service import BuyPackageService
from src.payment.services.my_payments.my_payments_service import MyPaymentsService
from src.payment.services.payment_webhook.payment_webhook_service import PaymentWebhookService
from src.payment.services.spendings.can_spend_service import CanSpendService
from src.user.models import User


@require_GET
@login_required
def my_spendings(request: HttpRequest) -> HttpResponse:
    get = request.GET
    page = int(get.get('page', 1))
    user = request.user

    service = MyPaymentsService()
    spendings = service.get_my_spendings(user=user, current_page=page)
    balance = Balance.get_user_balance(user)

    return render(
        request,
        'my_spendings.html',
        {
            'spendings': spendings,
            'balance': balance,
            'current_user': user
        },
    )


@require_GET
@login_required
def api_get_balance(request: HttpRequest) -> JsonResponse:
    user: User = request.user
    balance: Balance = Balance.objects.get(user=user)
    status = 'ok'
    if balance.balance < 100:
        status = 'low_balance'

    return JsonResponse({'balance': balance.balance, 'status': status})


@require_GET
@login_required
def list_packages(request: HttpRequest) -> HttpResponse:
    context = {
        'packages': Package.objects.all(),
    }
    return render(request, 'list_packages.html', context)


@require_POST
@login_required
def buy_single_package(request: HttpRequest, package_id: int) -> HttpResponse:
    service = BuyPackageService()
    redirect_url = service.buy_package(request.user, package_id)
    return redirect(redirect_url)


@require_POST
@csrf_exempt
def payment_webhook(request: HttpRequest) -> JsonResponse:
    if request.content_type == 'application/json':
        data = json.loads(request.body)
    else:
        data = request.POST.dict()

    log.info(data)  # @TODO remove log
    webhook_service = PaymentWebhookService()
    webhook_service.handle_webook(data)
    return JsonResponse({})


@require_POST
def api_can_purchase(request: HttpRequest) -> JsonResponse:
    user: User | AnonymousUser = request.user
    if user.is_anonymous:
        return JsonResponse({'error': 'You are not authorized'}, status=401)

    body = json.loads(request.body)
    service = CanSpendService()
    result = service.can_spend(user=user, type=body.get('type'))

    if result == False:
        return JsonResponse(
            {
                'error': f'Your balance is too low. <a href="{reverse_lazy('payment.list_packages')}" class="underline">Click here to buy more coins.</a>'
            },
            status=402
        )

    return JsonResponse({})
