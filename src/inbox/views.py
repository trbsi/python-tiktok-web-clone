from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
@login_required
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_home.html')
