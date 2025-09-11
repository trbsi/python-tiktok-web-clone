from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from src.engagement.services.like.like_service import LikeService


@require_POST
def like(request: HttpRequest, video_id: int) -> JsonResponse:
    if request.user.is_anonymous:
        return JsonResponse({})

    like_service = LikeService()
    like_service.toggle(video_id, request.user)
    return JsonResponse({})
