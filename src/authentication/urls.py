from django.urls import path

from .forms.register_form_view import RegisterFormView

urlpatterns = [
    path('register', RegisterFormView.as_view(), name='register'),
]
