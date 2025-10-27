from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET

from src.notification.services.notification_service import NotificationService
from src.notification.value_objects.email_value_object import EmailValueObject


@require_GET
def terms_of_use(request: HttpRequest) -> HttpResponse:
    return render(request, 'terms_of_use.html')


@require_GET
def privacy_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'privacy_policy.html')


@require_GET
def content_moderation_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'content_moderation_policy.html')


@require_GET
def send_test_email(request: HttpRequest) -> HttpResponse:
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
