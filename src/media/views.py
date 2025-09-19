from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from src.media.services.upload_media_service import UploadMediaService


@require_GET
@login_required
def upload(request: HttpRequest) -> HttpResponse:
    return render(request, 'upload.html')


@require_POST
@login_required
def do_upload(request: HttpRequest) -> JsonResponse:
    file = request.FILES.get('file')
    service = UploadMediaService()
    service.upload(file)
    
    return JsonResponse({})
