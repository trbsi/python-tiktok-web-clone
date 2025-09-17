from django.core.paginator import Paginator, Page
from django.db.models import QuerySet

from src.engagement.models import Like
from src.media.models import Media
from src.user.models import User


class UserMediaService:
    PER_PAGE = 10

    def get_user_media(self, username: str, current_page: int) -> dict:
        user: User = User.objects.get(username=username)
        media: QuerySet[Media] = Media.objects.filter(user=user).order_by('-created_at')

        paginator = Paginator(object_list=media, per_page=self.PER_PAGE)
        page: Page = paginator.page(current_page)

        result = []
        for media_item in page.object_list:
            result.append({
                'id': media_item.id,
                'thumbnail': str(media_item.file_thumbnail),
            })

        next_page = page.next_page_number() if page.has_next() else None

        return {'result': result, 'next_page': next_page}

    def get_user_liked_media(self, username: str, current_page: int) -> dict:
        user: User = User.objects.get(username=username)
        likes: QuerySet[Like] = Like.objects.filter(user=user).order_by('-created_at')

        paginator = Paginator(object_list=likes, per_page=self.PER_PAGE)
        page: Page = paginator.page(current_page)

        media_ids = page.object_list.values_list('media_id', flat=True)
        media = Media.objects.filter(id__in=media_ids).order_by('-created_at')

        result = []
        for media_item in media:
            result.append({
                'id': media_item.id,
                'thumbnail': str(media_item.file_thumbnail),
            })

        next_page = page.next_page_number() if page.has_next() else None

        return {'result': result, 'next_page': next_page}
