from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'feed_home.html')
