from django.core.paginator import Paginator, Page
from django.urls import reverse_lazy

from src.core.utils import full_url_for_path
from src.media.enums import MediaEnum
from src.media.models import Media
from src.payment.utils import coin_to_fiat
from src.user.models import User


class MyContentService:
    PER_PAGE = 25

    def list_my_content(self, user: User, current_page: int) -> Page[Media]:
        media = (
            Media.objects
            .filter(user=user)
            .exclude(status=MediaEnum.STATUS_DELETED.value)
            .order_by('-id')
        )
        paginator = Paginator(object_list=media, per_page=self.PER_PAGE)
        page: Page = paginator.page(current_page)

        for item in page.object_list:
            item.consent_url = full_url_for_path(
                reverse_lazy('consent.request_consent', kwargs={'media_id': item.id})
            )
            item.unlock_price = coin_to_fiat(item.unlock_price)

        return page
