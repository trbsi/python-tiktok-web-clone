from django.urls import path

from . import views

urlpatterns = [
    path('api/follow-unfollow', views.follow_unfollow, name='follow.api.follow_unfollow'),
]
