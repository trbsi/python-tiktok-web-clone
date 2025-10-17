from allauth.account.signals import user_signed_up as allauth_user_signed_up, user_logged_in as allauth_user_logged_in
from django.contrib.auth.signals import user_logged_in as django_user_logged_in
from django.dispatch import receiver

from src.authentication.services.post_auth.post_login_service import PostLoginService
from src.authentication.services.post_auth.post_registration_service import PostRegistrationService
from src.core.utils import get_client_ip


@receiver(allauth_user_signed_up)
def after_signup(request, user, **kwargs):
    """
    This is triggered after allauth signup
    """
    service = PostRegistrationService()
    ip = get_client_ip(request)
    service.post_register(user, ip)


@receiver(allauth_user_logged_in)
@receiver(django_user_logged_in)
def after_login(request, user, **kwargs):
    """
    This is triggered after allauth and django login
    """
    service = PostLoginService()
    ip = get_client_ip(request)
    service.post_login(user, ip)
