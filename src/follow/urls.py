from django.urls import path

from . import views

urlpatterns = [
    path('api/follow-unfollow', views.api_follow_unfollow, name='follow.api.follow_unfollow'),
]
