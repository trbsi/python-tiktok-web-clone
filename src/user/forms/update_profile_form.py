from PIL import Image
from django import forms

from src.user.models import UserProfile


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_image')

    def resize_image(self):
        if self.instance.profile_image is None:
            return

        image_path = self.instance.profile_image.path
        image = Image.open(image_path)
        image.thumbnail((300, 300))
        image.save(image_path)
        print(image_path)
