import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from app import settings
from src.notification.services.subscribe.push_subscribe_service import PushSubscribeService


@require_GET
def api_web_push_keys(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        'public_key': settings.WEB_PUSH_PUBLIC_KEY
    })


@require_POST
@login_required
def api_subscribe(request: HttpRequest) -> JsonResponse:
    body = json.load(request.body)
    
    service = PushSubscribeService()
    service.push_subscribe(request.user, body)

    return JsonResponse({})
