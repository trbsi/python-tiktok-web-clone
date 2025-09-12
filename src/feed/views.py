from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from src.feed.services.load_feed_service import LoadFeedService


@require_GET
def discover(request: HttpRequest) -> HttpResponse:
    return render(request, 'feed_home.html')


@require_GET
def following(request: HttpRequest) -> HttpResponse:
    return render(request, 'feed_home.html')


@require_GET
def feed(request: HttpRequest) -> JsonResponse:
    data = request.GET
    page = int(data.get('page'))

    service: LoadFeedService = LoadFeedService()
    items: list = service.get_feed_items(
        page=page,
        user=request.user
    )
    return JsonResponse({
        'results': items,
        'next_page': page + 1,
    })
