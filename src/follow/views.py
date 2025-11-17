import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_POST

from src.follow.services.follow.follow_service import FollowService


@require_POST
@login_required
def api_follow_unfollow(request: HttpRequest) -> JsonResponse:
    post = json.loads(request.body)

    service = FollowService()
    result = service.follow_unfollow(follower=request.user, following=int(post.get('following')))

    return JsonResponse({'status': result})
