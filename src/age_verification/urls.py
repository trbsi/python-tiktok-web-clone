from django.urls import path

from . import views

urlpatterns = [
    path('performer-agreement', views.performer_agreement, name='age_verification.performer_agreement'),
    path('kyc', views.kyc, name='age_verification.kyc'),
    path('become-performer', views.become_performer, name='age_verification.become_performer'),
]
