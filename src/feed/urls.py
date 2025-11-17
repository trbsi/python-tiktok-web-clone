from django.urls import path

from . import views

urlpatterns = [
    path('discover/grid', views.discover_grid, name='feed.discover.grid'),
    path('discover/scroll', views.discover_scroll, name='feed.discover.scroll'),
    path('following', views.following, name='feed.following'),
    path('api/media', views.api_get_feed, name='feed.api.get_media'),
]
