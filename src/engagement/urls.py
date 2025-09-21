from django.urls import path

from . import views

urlpatterns = [
    path('api/like/media/<int:media_id>', views.like),
    path('api/comments/media/<int:media_id>', views.list_comments),
    path('api/comments', views.create_comment, name='engagement.api.create_comment')
]
