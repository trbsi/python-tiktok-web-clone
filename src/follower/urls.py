from django.urls import path

from . import views

urlpatterns = [
    path('api/follow/<int:user_id>', views.follow),
]
