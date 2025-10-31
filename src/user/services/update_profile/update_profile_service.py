from PIL import Image

from src.user.forms.update_profile_form import UpdateProfileForm
from src.user.models import UserProfile


class UpdateProfileService:
    def update_profile(self, form: UpdateProfileForm) -> bool:
        if form.is_valid():
            form.save()
            self._resize_image(instance=form.instance)
            return True

        return False

    def _resize_image(self, instance: UserProfile):
        if not instance.profile_image:
            return

        image_path = instance.profile_image.path
        image = Image.open(image_path)
        image.thumbnail((300, 300))
        image.save(image_path)
