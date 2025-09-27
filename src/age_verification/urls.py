from django.urls import path

from . import views

urlpatterns = [
    path('creator-agreement', views.creator_agreement, name='age_verification.creator_agreement'),
    path('kyc', views.kyc, name='age_verification.kyc'),
    path('become-creator', views.become_creator, name='age_verification.become_creator'),
]
