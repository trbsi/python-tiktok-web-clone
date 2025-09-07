from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from src.feed.services.load_videos_service import LoadVideosService


@require_GET
def fyp(request: HttpRequest) -> HttpResponse:
    return render(request, 'feed_home.html')


@require_GET
def following(request: HttpRequest) -> HttpResponse:
    return render(request, 'feed_home.html')


@require_GET
def videos(request: HttpRequest) -> JsonResponse:
    data = request.GET
    page = int(data.get('page'))
    per_page = int(data.get('per_page'))
    
    service: LoadVideosService = LoadVideosService(
        per_page=per_page,
        page=page
    )
    videos: list = service.get_videos()
    return JsonResponse({
        'results': videos,
        'next_page': page + 1,
    })
