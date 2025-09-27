from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST

from src.age_verification.services.creator_service import CreatorService
from src.media.services.upload_media.upload_media_service import UploadMediaService
from src.user.models import User


@require_GET
@login_required
def upload(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    if user.is_regular_user():
        raise PermissionDenied

    is_creator = user.is_creator()
    if is_creator or is_creator == False:
        if not _can_access_upload(request):
            return redirect(reverse_lazy('age_verification.become_creator'))

    return render(request, 'upload.html')


@require_POST
@login_required
def do_upload(request: HttpRequest) -> JsonResponse:
    user: User = request.user
    if user.is_regular_user():
        raise PermissionDenied

    is_creator = user.is_creator()
    if is_creator or is_creator == False:
        if not _can_access_upload(request):
            return redirect(reverse_lazy('age_verification.become_creator'))

    files = request.FILES.get('files')
    service = UploadMediaService()
    service.upload(files)

    return JsonResponse({})


def _can_access_upload(request: HttpRequest) -> bool:
    service = CreatorService()
    age_verification = service.is_age_verification_completed(request.user)
    agreement = service.is_creator_agreement_completed(request.user)

    if not age_verification and not agreement:
        messages.warning(request, 'You have to sign creator agreement and verify your age')
        return False
    else:
        return True
