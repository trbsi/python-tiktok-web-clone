from src.user.models import User


class UserSearchService:
    def search_user(self, query: str) -> list:
        users = User.objects.filter(username__icontains=query)[:5]
        result = []
        for user in users:
            result.append(user.username)

        return result
