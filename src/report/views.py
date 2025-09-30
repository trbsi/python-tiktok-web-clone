import json

from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from src.report.services.report.report_service import ReportService


@require_POST
def api_report(request: HttpRequest) -> JsonResponse:
    service = ReportService()
    data = json.loads(request.body)
    service.report(type=data.get('type'), content_id=int(data.get('content_id')), user=request.user)
    return JsonResponse({})


@require_POST
def report(request: HttpRequest) -> HttpResponse:
    service = ReportService()
    data = request.POST
    service.report(type=data.get('type'), content_id=int(data.get('content_id')), user=request.user)

    messages.success(request, 'Report successfully sent')
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)
