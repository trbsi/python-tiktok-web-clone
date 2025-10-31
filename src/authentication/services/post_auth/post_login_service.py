from src.core.utils import get_ip_data
from src.user.models import User, UserProfile


class PostLoginService:
    def post_login(self, user: User, ip: str) -> None:
        ip_data = get_ip_data(ip)
        if ip_data.timezone:
            profile: UserProfile = user.profile
            profile.timezone = ip_data.timezone
            profile.country_code = ip_data.country_code
            profile.state_code = ip_data.state_code
            profile.save()
