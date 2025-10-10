from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from src.authentication.services.post_registration_service import PostRegistrationService
from src.core.utils import get_client_ip
from src.user.models import User as User

alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$',
    'Username must contain only letters and numbers.'
)


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, validators=[alphanumeric])
    email = forms.EmailField()
    accept_tos = forms.BooleanField(required=True, label='I accept Terms Of Use')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # extract request
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'accept_tos']

    def save(self, commit=True):
        post_registration_service = PostRegistrationService()
        user = super().save(commit)

        ip = get_client_ip(self.request)
        post_registration_service.post_register(user, ip)

        return user
