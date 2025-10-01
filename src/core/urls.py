from django.urls import path

from src.feed import views as feed_views
from . import views

urlpatterns = [
    path('', feed_views.discover, name='home'),
    path('terms-of-use', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('content-moderation-policy', views.content_moderation_policy, name='content_moderation_policy'),
]
