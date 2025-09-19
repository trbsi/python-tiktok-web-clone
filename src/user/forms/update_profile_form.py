from django import forms

from src.user.models import UserProfile


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_image')
