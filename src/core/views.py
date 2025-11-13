from pathlib import Path

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app import settings
from src.core.utils import reverse_lazy_with_query
from src.notification.services.notification_service import NotificationService
from src.notification.value_objects.email_value_object import EmailValueObject


@require_GET
def legal_documents(request: HttpRequest) -> HttpResponse:
    document = request.GET.get('document')
    dir = Path(f'{settings.BASE_DIR}/static/legal_documents')
    files = []
    for file in dir.iterdir():
        if not file.is_file() or file.suffix != '.pdf':
            continue

        if document and document.lower() in file.name.lower():
            return redirect(f'/static/legal_documents/{file.name}')

        file_name = (
            file.name
            .replace('_', ' ')
            .replace('-', ' ')
            .replace('.pdf', '')
            .title())
        files.append({'file': file.name, 'name': file_name})

    return render(request, 'legal_documents.html', {'legal_documents': files})


@require_GET
def terms_of_use(request: HttpRequest) -> HttpResponse:
    return redirect(
        reverse_lazy_with_query(route_name='legal_documents', query_params={'document': 'terms_of_service'})
    )


@require_GET
def privacy_policy(request: HttpRequest) -> HttpResponse:
    return redirect(
        reverse_lazy_with_query(route_name='legal_documents', query_params={'document': 'privacy_policy'})
    )


@require_GET
def test_notifications(request: HttpRequest) -> HttpResponse:
    email = EmailValueObject(
        subject='Test Email',
        template_path='emails/test_email.html',
        template_variables={'anchor_href': 'www.test.com', 'anchor_label': 'Click here to confirm your new email'},
        to=['admins']
    )
    NotificationService.send_notification(email)
    messages.success(request, 'Thank you for sending an email')
    return redirect(reverse_lazy('home'))


@require_GET
def landing_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing_page.html')
