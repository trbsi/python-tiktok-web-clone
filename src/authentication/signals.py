from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from src.authentication.services.post_registration_service import PostRegistrationService
from src.core.utils import get_client_ip


@receiver(user_signed_up)
def after_signup(request, user, **kwargs):
    """
    This is triggered after allauth signup
    """
    service = PostRegistrationService()
    ip = get_client_ip(request)
    service.post_register(user, ip)
