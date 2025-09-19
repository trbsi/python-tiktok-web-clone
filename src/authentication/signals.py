from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from src.user.models import UserProfile


@receiver(user_signed_up)
def after_signup(request, user, **kwargs):
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user)
