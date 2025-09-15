from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def terms_of_use(request: HttpRequest) -> HttpResponse:
    return render(request, 'terms_of_use.html')


def privacy_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'privacy_policy.html')


def content_moderation_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'content_moderation_policy.html')
