from django.core.paginator import Paginator

from src.follower.models import Follow
from src.user.models import User


class UserFollowingService:
    PER_PAGE = 10

    def get_following(self, user: User, current_page: int) -> dict:
        following = Follow.get_following(user)
        paginator = Paginator(object_list=following, per_page=self.PER_PAGE)
        page = paginator.page(current_page)

        result = []
        for user in page.object_list:
            result.append({
                'id': user.id,
                'title': user.username,
                'thumbnail': str(user.get_profile_image()),
            })

        next_page = page.next_page_number() if page.has_next() else None

        return {'result': page.object_list, 'next_page': next_page}
