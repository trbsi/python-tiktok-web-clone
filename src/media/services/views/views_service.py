from django.contrib.auth.models import AnonymousUser

from src.media.models import Media, Views
from src.user.models import User


class ViewsService:
    def record_view(self, user:User|AnonymousUser, media_id:int) -> None:
        media:Media= Media.objects.get(id=media_id)
        media.view_count += 1
        media.save()

        if user.is_authenticated:
            Views.objects.create(
                media=media,
                user=user,
            )