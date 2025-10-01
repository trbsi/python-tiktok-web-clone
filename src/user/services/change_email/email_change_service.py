import secrets

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse

from src.notification.services.notification_service import NotificationService
from src.notification.value_objects.email_value_object import EmailValueObject
from src.user.models import User, EmailChangeToken


class EmailChangeService():
    def request_email_change(self, request: HttpRequest, user: User, new_email: str) -> None:
        token = secrets.token_urlsafe(32)

        EmailChangeToken.objects.create(
            user=user,
            new_email=new_email,
            token=token,
        )

        confirm_url = request.build_absolute_uri(
            reverse("user.confirm_email_change", kwargs={"token": token})
        )

        email = EmailValueObject(
            subject="Confirm your new email",
            template_path='emails/auth/update_email.html',
            template_variables={'confirm_url': confirm_url},
            to=[new_email]
        )
        NotificationService.send_notification(email)

    def get_email_change(self, token: str) -> EmailChangeToken:
        return get_object_or_404(EmailChangeToken, token=token)

    def change_email(self, change: EmailChangeToken) -> None:
        # Apply the new email
        user = change.user
        user.email = change.new_email
        user.save()

        # Clean up
        change.delete()
