from django.urls import path

from . import views

urlpatterns = [
    path('', views.upload, name='media.upload'),
    path('do-upload', views.do_upload, name='media.do_upload'),
]
