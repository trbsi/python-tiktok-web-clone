from django.urls import path

from . import views

urlpatterns = [
    path('delete', views.delete, name='user.delete'),
    path('do-delete', views.do_delete, name='user.do_delete'),
    path('update-email', views.update_email, name='user.update_email'),
    path('update-profile', views.update_profile, name='user.update_profile'),
    path('confirm-email-change/<str:token>', views.confirm_email_change, name='user.confirm_email_change'),

    path('api/get-media', views.api_get_user_media, name='user.api.get_media'),
    path('api/get-liked-media', views.api_get_user_liked_media, name='user.api.get_liked_media'),
    path('api/get-following', views.api_get_following, name='user.api.get_following'),
    path('api/search', views.api_user_search, name='user.api.user_search'),

    path('<str:username>', views.profile, name='user.profile'),
    path('<str:username>/liked', views.profile_liked_media, name='user.profile.liked_media'),
]
