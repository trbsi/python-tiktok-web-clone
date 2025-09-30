from django.core.paginator import Paginator, Page

from src.media.models import Media
from src.user.models import User


class MyContentService:
    PER_PAGE = 25

    def list_my_content(self, user: User, current_page: int) -> Page[Media]:
        media = Media.objects.filter(user=user).order_by('-id')
        paginator = Paginator(object_list=media, per_page=self.PER_PAGE)
        page = paginator.page(current_page)

        return page
