from django.urls import path

from . import views

urlpatterns = [
    path('api/like/<int:video_id>', views.like),
]
