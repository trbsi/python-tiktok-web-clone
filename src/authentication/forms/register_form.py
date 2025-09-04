from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

ROLES = [
    ('user', 'User'),
    ('performer', 'Performer'),
]


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=ROLES, required=True)
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
        return user
