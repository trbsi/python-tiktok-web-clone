from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def fyp(request: HttpRequest) -> HttpResponse:
    return render(request, 'feed_temp.html')


def following(request: HttpRequest) -> HttpResponse:
    return render(request, 'feed_temp.html')
