from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST


@require_GET
@login_required
def list_conversations(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_conversations.html')


@require_GET
@login_required
def list_messages(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_messages.html')


# GET and POST
@login_required
def send_message(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_message.html')


@require_GET
@login_required
def api_list_conversations(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_conversations_api.html')


@require_GET
@login_required
def api_list_messages(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_conversations_messages.html')


@require_POST
@login_required
def api_send_message(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_messages.html')


@require_GET
@login_required
def api_polling_messages(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_poll.html')


@require_POST
@login_required
def delete(request: HttpRequest) -> HttpResponse:
    return render(request, 'inbox_delete.html')
