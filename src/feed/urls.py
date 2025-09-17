from django.urls import path

from . import views

urlpatterns = [
    path('discover', views.discover, name='feed.discover'),
    path('following', views.following, name='feed.following'),
    path('api/media', views.api_get_feed, name='feed.api.get_media'),
]
