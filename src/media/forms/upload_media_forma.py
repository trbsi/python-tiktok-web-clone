from django import forms

from src.media.models import Media


class UploadMediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('file')
