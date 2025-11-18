from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET

from src.feed.services.load_feed_service import LoadFeedService


@require_GET
def discover_scroll(request: HttpRequest) -> HttpResponse:
    get = request.GET
    filters = _get_filters(request)

    return render(
        request,
        'feed.html',
        {
            'type': LoadFeedService.FEED_TYPE_DISCOVER,
            'filters': ','.join(filters),
            # When user comes from  discover page or profile to scroll page
            'go_back_button': bool(get.get('go_back', False)),
            'media_api_url': reverse_lazy('feed.api.get_media'),
            'follow_unfollow_api': reverse_lazy('follow.api.follow_unfollow'),
            'create_comment_api': reverse_lazy('engagement.api.create_comment'),
            'report_content_api': reverse_lazy('report.api.report_content'),
            'like_media_api': reverse_lazy('engagement.api.like_media', kwargs={'media_id': '__MEDIA_ID__'}),
            'list_comments_api': reverse_lazy('engagement.api.list_comments', kwargs={'media_id': '__MEDIA_ID__'}),
            'unlock_media_api': reverse_lazy('media.api.unlock'),
            'record_views_api': reverse_lazy('media.api.record_views'),
            'is_authenticated': 1 if request.user.is_authenticated else 0,
        }
    )


@require_GET
def discover_grid(request: HttpRequest) -> HttpResponse:
    get = request.GET
    filters = _get_filters(request)

    return render(
        request,
        'discover_grid.html',
        {
            'discover_feed_url': reverse_lazy('feed.discover.grid'),
            'media_api_url': reverse_lazy('feed.api.get_media'),
            'filters': ','.join(filters),
            'query': get.get('query', ''),
            'go_back_button': bool(get.get('go_back', False)),
        }
    )


@require_GET
def following(request: HttpRequest) -> HttpResponse:
    get = request.GET
    filters = _get_filters(request)

    return render(
        request,
        'feed.html',
        {
            'type': LoadFeedService.FEED_TYPE_FOLLOW,
            'filters': ','.join(filters),
            # When user comes from  discover page or profile to scroll page
            'go_back_button': bool(get.get('go_back', False)),
            'user': request.user,
            'media_api_url': reverse_lazy('feed.api.get_media'),
            'follow_unfollow_api': reverse_lazy('follow.api.follow_unfollow'),
            'create_comment_api': reverse_lazy('engagement.api.create_comment'),
            'report_content_api': reverse_lazy('report.api.report_content'),
            'like_media_api': reverse_lazy('engagement.api.like_media', kwargs={'media_id': '__MEDIA_ID__'}),
            'list_comments_api': reverse_lazy('engagement.api.list_comments', kwargs={'media_id': '__MEDIA_ID__'}),
            'unlock_media_api': reverse_lazy('media.api.unlock'),
            'record_views_api': reverse_lazy('media.api.record_views'),
            'is_authenticated': 1 if request.user.is_authenticated else 0,
        }
    )


@require_GET
def api_get_feed(request: HttpRequest) -> JsonResponse:
    requestData = request.GET
    page = int(requestData.get('page'))
    type = requestData.get('type')
    filters = requestData.get('filters')

    service: LoadFeedService = LoadFeedService()

    if type == LoadFeedService.FEED_TYPE_FOLLOW:
        data: dict = service.get_following_feed(page=page, user=request.user, filters=filters)
    else:
        data: dict = service.get_discover_feed(page=page, user=request.user, filters=filters)

    return JsonResponse({
        'results': data['result'],
        'next_page': data['next_page'],
    })


def _get_filters(request: HttpRequest) -> list:
    get = request.GET
    user_id = get.get('uid')
    media_id = get.get('mid')
    hashtag = get.get('hashtag')
    query = get.get('query')
    filters = []

    if user_id:
        filters.extend(['uid', user_id])

    if media_id:
        filters.extend(['mid', media_id])

    if hashtag:
        filters.extend(['hashtag', hashtag])

    if query:
        filters.extend(['query', query])

    return filters
