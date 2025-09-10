from django.urls import path

from . import views

urlpatterns = [
    path('discover', views.discover, name='feed.discover'),
    path('following', views.following, name='feed.following'),
    path('api/videos', views.videos),
]
