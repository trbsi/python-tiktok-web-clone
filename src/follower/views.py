from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from src.follower.services.follow.follow_service import FollowService


# TODO finish
@require_POST
@login_required
def follow(request, user_id: int) -> JsonResponse:
    service = FollowService()
    service.follow(user=request.user, user_id=user_id)
