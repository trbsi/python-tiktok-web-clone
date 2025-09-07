from django.core.paginator import Paginator

from src.media.models import Media


class LoadVideosService:
    def __init__(self, per_page: int, page: int):
        self.per_page = per_page
        self.page = page

    def get_videos(self) -> list:
        items = Media.objects.all()
        paginator = Paginator(object_list=items, per_page=self.per_page)
        page = paginator.page(self.page)
        result = []
        for item in page.object_list:
            result.append({
                'id': item.id,
                'likes': item.like_count,
                'comments_count': item.comment_count,
                'description': item.description,
                'liked': False,
                'user': {
                    'username': item.user.username,
                    'avatar': str(item.user.profile.profile_image),
                },
            })

        return result
