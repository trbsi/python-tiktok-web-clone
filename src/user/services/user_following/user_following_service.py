from django.core.paginator import Paginator
from django.urls import reverse_lazy

from src.follow.models import Follow
from src.user.models import User


class UserFollowingService:
    PER_PAGE = 10

    def get_following(self, user: User, current_page: int) -> dict:
        following = Follow.get_following(user)
        paginator = Paginator(object_list=following, per_page=self.PER_PAGE)
        page = paginator.page(current_page)

        result = []
        for user_data in page.object_list:
            result.append({
                'id': user_data.id,
                'title': user_data.username,
                'thumbnail': str(user_data.get_profile_picture()),
                'item_type': 'creator_profile',
                'destination_url': reverse_lazy('user.profile', kwargs={'username': user_data.username}),
            })

        next_page = page.next_page_number() if page.has_next() else None

        return {'result': result, 'next_page': next_page}
