import json

from django.http import HttpRequest, JsonResponse

from src.report.services.report.report_service import ReportService


def report(request: HttpRequest) -> JsonResponse:
    service = ReportService()
    data = json.loads(request.body)
    service.report(type=data.get('type'), content_id=int(data.get('content_id')), user=request.user)
    return JsonResponse({})
