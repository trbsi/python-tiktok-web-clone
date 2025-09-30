from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from src.authentication.services.post_registration_service import PostRegistrationService

"""
After allauth signup
"""


@receiver(user_signed_up)
def after_signup(request, user, **kwargs):
    service = PostRegistrationService()
    service.post_register(user)
