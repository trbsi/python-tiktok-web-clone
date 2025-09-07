from django.urls import path

from . import views

urlpatterns = [
    path('fyp', views.fyp, name='feed.fyp'),
    path('following', views.following, name='feed.following'),
    path('api/videos', views.videos),
]
