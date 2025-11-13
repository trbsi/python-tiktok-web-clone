from django.core.paginator import Paginator, Page
from django.db.models import QuerySet

from src.core.utils import reverse_lazy_with_query
from src.engagement.models import Like
from src.media.enums import MediaEnum
from src.media.models import Media
from src.user.models import User


class UserMediaService:
    PER_PAGE = 9

    def get_user_media(self, username: str, current_page: int) -> dict:
        user: User = User.objects.get(username=username)
        media: QuerySet[Media] = (
            Media.objects
            .filter(status=MediaEnum.STATUS_PAID.value)
            .filter(is_approved=True)
            .filter(user=user).order_by('-created_at')
        )

        paginator = Paginator(object_list=media, per_page=self.PER_PAGE)
        page: Page = paginator.page(current_page)

        result = []
        for media_item in page.object_list:
            result.append({
                'id': media_item.id,
                'title': '',
                'thumbnail': str(
                    media_item.get_thumbnail_url()) if media_item.is_video() else media_item.get_file_url(),
                'item_type': media_item.file_type,
                'destination_url': reverse_lazy_with_query(
                    route_name='feed.following',
                    kwargs=None,
                    query_params={'uid': user.id, 'mid': media_item.id},
                ),
            })

        next_page = page.next_page_number() if page.has_next() else None

        return {'result': result, 'next_page': next_page}

    def get_user_liked_media(self, username: str, current_page: int) -> dict:
        user: User = User.objects.get(username=username)
        likes: QuerySet[Like] = Like.objects.filter(user=user).order_by('-created_at')

        paginator = Paginator(object_list=likes, per_page=self.PER_PAGE)
        page: Page = paginator.page(current_page)

        media_ids = list(page.object_list.values_list('media_id', flat=True))
        media = Media.objects.select_related('user').filter(id__in=media_ids).order_by('-created_at')

        result = []
        for media_item in media:
            result.append({
                'id': media_item.id,
                'title': media_item.user.username,
                'thumbnail': str(media_item.get_thumbnail_url()),
                'item_type': media_item.file_type,
                'destination_url': reverse_lazy_with_query(
                    route_name='feed.following',
                    kwargs=None,
                    query_params={'uid': media_item.user.id, 'mid': media_item.id},
                ),
            })

        next_page = page.next_page_number() if page.has_next() else None

        return {'result': result, 'next_page': next_page}
