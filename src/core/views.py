import random
from pathlib import Path

import bugsnag
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET

from app import settings
from src.core.utils import reverse_lazy_with_query, reverse_lazy_admin
from src.media.models import Media
from src.notification.services.notification_service import NotificationService
from src.notification.value_objects.email_value_object import EmailValueObject
from src.notification.value_objects.push_notification_value_object import PushNotificationValueObject
from src.user.models import User


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
    only = request.GET.get('only')
    for_user = request.GET.get('for_user')
    push = []

    if for_user:
        user = User.objects.get(username=for_user)
    else:
        user = User.objects.get(username='dinamo')

    if only == 'push':
        push.append(PushNotificationValueObject(
            user_id=user.id,
            body=f'This is test push notification {random.randint(1, 100000)}'
        ))
    elif only == 'email':
        push.append(EmailValueObject(
            subject='Test Email',
            template_path='emails/test_email.html',
            template_variables={'anchor_href': 'www.test.com', 'anchor_label': 'Click here to confirm your new email'},
            to=['admins']
        ))
    else:
        url = reverse_lazy_admin(object=Media(), action='changelist', is_full_url=True)
        push.append(EmailValueObject(
            subject='Test Email',
            template_path='emails/test_email.html',
            template_variables={'anchor_href': 'www.test.com', 'anchor_label': 'Click here to confirm your new email'},
            to=['admins']
        ))
        push.append(PushNotificationValueObject(
            user_id=user.id,
            body=f'This is test push notification {random.randint(1, 100000)}. {url}'
        ))

        bugsnag.notify(Exception(f'This is test error {random.randint(1, 100000)}'))

    NotificationService.send_notification(*push)

    messages.success(request, 'Thank you for sending an email')
    return redirect(reverse_lazy('home'))


@require_GET
def landing_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing_page.html')
