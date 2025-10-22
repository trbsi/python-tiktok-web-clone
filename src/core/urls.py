from django.urls import path

from . import views

urlpatterns = [
    # path('', feed_views.following, name='home'),
    path('', views.landing_page, name='home'),
    path('terms-of-use', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('content-moderation-policy', views.content_moderation_policy, name='content_moderation_policy'),
    path('send-test-email', views.send_test_email, name='send_test_email'),
]
