import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST, require_GET

from src.engagement.services.comment_create.create_comment import CreateComment
from src.engagement.services.comment_list.comment_list_service import CommentListService
from src.engagement.services.like.like_service import LikeService


@require_POST
def like(request: HttpRequest, media_id: int) -> JsonResponse:
    if request.user.is_anonymous:
        return JsonResponse({})

    like_service = LikeService()
    like_service.toggle(media_id, request.user)
    return JsonResponse({})


@require_GET
def list_comments(request: HttpRequest, media_id: int) -> JsonResponse:
    service = CommentListService()
    comments = service.list(media_id)
    return JsonResponse({'results': comments})


@require_POST
@login_required
def create_comment(request: HttpRequest) -> JsonResponse:
    post = json.loads(request.body)
    service = CreateComment()
    comment: dict = service.create_comment(
        user=request.user,
        comment=post.get('comment'),
        media_id=int(post.get('media_id'))
    )

    return JsonResponse(comment)
