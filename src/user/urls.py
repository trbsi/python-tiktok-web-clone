from django.urls import path

from . import views

urlpatterns = [
    path('delete', views.delete, name='user.delete'),
    path('do-delete', views.do_delete, name='user.do_delete'),
    path('<str:username>', views.profile, name='user.profile'),
    path('<str:username>/liked', views.profile_liked_media, name='user.profile.liked_media'),
    path('get-media', views.get_user_media, name='user.get_media'),
    path('get-liked-media', views.get_user_liked_media, name='user.get_liked_media'),
]
