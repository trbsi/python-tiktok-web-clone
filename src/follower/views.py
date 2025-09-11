from django.http import JsonResponse

from src.follower.services.follow.follow_service import FollowService


def follow(request, user_id:int)->JsonResponse:
    service = FollowService()
    service.follow(user=request.user, user_id=user_id)