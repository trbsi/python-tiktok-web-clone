from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def upload(request: HttpRequest) -> HttpResponse:
    return render(request, 'upload.html')
