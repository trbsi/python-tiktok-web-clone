from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def profile(request: HttpRequest, username: str) -> HttpResponse:
    return render(request, 'profile.html')
