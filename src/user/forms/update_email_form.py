from django import forms

from src.user.models import User


class UpdateEmailForm(forms.Form):
    email = forms.EmailField(label='Email Address', max_length=100, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered')

        return email
