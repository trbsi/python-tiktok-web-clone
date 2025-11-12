from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET

from src.feed.services.load_feed_service import LoadFeedService


@require_GET
def discover(request: HttpRequest) -> HttpResponse:
    filters = _get_filters(request)
    return render(
        request,
        'feed_home.html',
        {
            'type': 'discover',
            'filters': ','.join(filters),
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
def following(request: HttpRequest) -> HttpResponse:
    filters = _get_filters(request)
    return render(
        request,
        'feed_home.html',
        {
            'type': 'following',
            'filters': ','.join(filters),
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


def _get_filters(request: HttpRequest) -> list:
    get = request.GET
    user_id = get.get('uid')
    media_id = get.get('mid')
    hashtag = get.get('hashtag')
    filters = []

    if user_id:
        filters.extend(['uid', user_id])

    if media_id:
        filters.extend(['mid', media_id])

    if hashtag:
        filters.extend(['hashtag', hashtag])

    return filters


@require_GET
def api_get_feed(request: HttpRequest) -> JsonResponse:
    requestData = request.GET
    page = int(requestData.get('page'))
    type = requestData.get('type')
    filters = requestData.get('filters')

    service: LoadFeedService = LoadFeedService()

    if type == 'following':
        data: dict = service.get_following_feed(page=page, user=request.user, filters=filters)
    else:
        data: dict = service.get_discover_feed(page=page, user=request.user)

    return JsonResponse({
        'results': data['result'],
        'next_page': data['next_page'],
    })
