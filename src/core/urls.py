from django.urls import path

from src.feed import views as feed_views
from . import views

urlpatterns = [
    path('', feed_views.following, name='home'),
    path('about', views.landing_page, name='about'),
    path('terms-of-use', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('legal-documents', views.legal_documents, name='legal_documents'),
    path('send-test-email', views.send_test_email, name='send_test_email'),
]
