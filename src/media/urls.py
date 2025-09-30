from django.urls import path

from . import views

urlpatterns = [
    path('upload', views.upload, name='media.upload'),
    path('api/upload', views.api_upload, name='media.api.upload'),
    path('my-content', views.my_content, name='media.my_content'),
    path('update-my-media', views.update_my_media, name='media.update_my_media'),
]
