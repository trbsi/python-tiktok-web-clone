from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST

from src.age_verification.models import CreatorAgreement, Kyc
from src.media.services.upload_media.upload_media_service import UploadMediaService
from src.user.models import User


@require_GET
@login_required
def upload(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    if user.is_regular_user():
        raise PermissionDenied

    if user.is_creator():
        _can_creator_access(request)

    return render(request, 'upload.html')


@require_POST
@login_required
def do_upload(request: HttpRequest) -> JsonResponse:
    user: User = request.user
    if user.is_regular_user():
        raise PermissionDenied

    if user.is_creator():
        _can_creator_access(request)

    files = request.FILES.get('files')
    service = UploadMediaService()
    service.upload(files)

    return JsonResponse({})


def _can_creator_access(request: HttpRequest):
    agreement = CreatorAgreement.objects.filter(user=request.user).exists()
    kyc = Kyc.objects.filter(user=request.user).exists()

    if not agreement and not kyc:
        messages.warning(request, 'You have to sign creator agreement and verify your age')
        return redirect(reverse_lazy('age_verification.become_creator'))
