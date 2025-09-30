from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from src.authentication.services.post_registration_service import PostRegistrationService
from src.user.models import User as User

alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$',
    'Username must contain only letters and numbers.'
)


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, validators=[alphanumeric])
    email = forms.EmailField()
    accept_tos = forms.BooleanField(required=True, label='I accept Terms Of Use')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'accept_tos']

    def save(self, commit=True):
        post_registration_service = PostRegistrationService()
        user = super().save(commit)
        post_registration_service.post_register(user)
        return user
