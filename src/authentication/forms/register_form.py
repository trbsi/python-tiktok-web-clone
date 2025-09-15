from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator

from src.user.enum import UserEnum
from src.user.models import User as User, UserProfile

alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$',
    'Username must contain only letters and numbers.'
)


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, validators=[alphanumeric])
    email = forms.EmailField()
    role = forms.ChoiceField(choices=UserEnum.roles(), required=True)
    accept_tos = forms.BooleanField(required=True, label='I accept Terms Of Use')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'accept_tos']

    def save(self, commit=True):
        user = super().save(commit)
        role = self.cleaned_data['role']
        if role == 'admin':
            role = 'user'
        Group.objects.get_or_create(name=role)
        user.groups.add(Group.objects.get(name=role))
        UserProfile.objects.create(user=user)
        return user
