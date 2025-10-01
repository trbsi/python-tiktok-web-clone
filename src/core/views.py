from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def terms_of_use(request: HttpRequest) -> HttpResponse:
    return render(request, 'terms_of_use.html')


@require_GET
def privacy_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'privacy_policy.html')


@require_GET
def content_moderation_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'content_moderation_policy.html')
