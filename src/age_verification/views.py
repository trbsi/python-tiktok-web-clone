from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from app.log import log
from src.age_verification.services.save_agreement_service import SaveAgreementService
from src.core.helpers import get_client_ip


@login_required
def become_creator(request: HttpRequest) -> HttpResponse:
    return render(request, 'age_verification/become_creator.html')


@login_required
def creator_agreement(request) -> HttpResponse:
    if request.method == 'POST':
        post = request.POST
        consent = post.get('consent')
        log.info(f'# TODO consent if {consent}')
        if consent == 'no':
            messages.error(request, 'You have to agree to the terms')
            return render(request, 'age_verification/creator_agreement.html')

        service = SaveAgreementService()
        service.save_agreement(
            user=request.user,
            ip=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        messages.success(request, 'Consent was successfully signed')

    return render(request, 'age_verification/creator_agreement.html')


@login_required
def kyc(request: HttpRequest) -> HttpResponse:
    return render(request, 'age_verification/kyc.html')
# TODO if performer registered through Twitter, role will not be assigned. Assign it after KYC and performer agreement
