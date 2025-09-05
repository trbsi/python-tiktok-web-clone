from django.urls import path

from src.feed import views as feed_views

urlpatterns = [
    path('', feed_views.fyp),
]
