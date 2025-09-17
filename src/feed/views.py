from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET

from src.feed.services.load_feed_service import LoadFeedService


@require_GET
def discover(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'feed_home.html',
        {'type': 'discover', 'media_api_url': reverse_lazy('feed.api.get_media')}
    )


@require_GET
def following(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'feed_home.html',
        {'type': 'following', 'media_api_url': reverse_lazy('feed.api.get_media')}
    )


@require_GET
def api_get_feed(request: HttpRequest) -> JsonResponse:
    requestData = request.GET
    page = int(requestData.get('page'))
    type = requestData.get('type')
    service: LoadFeedService = LoadFeedService()
    if type == 'following':
        data: dict = service.get_following_feed(page=page, user=request.user)
    else:
        data: dict = service.get_discover_feed(page=page, user=request.user)

    return JsonResponse({
        'results': data['result'],
        'next_page': data['next_page'],
    })
