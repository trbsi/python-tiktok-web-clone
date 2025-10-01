from django.urls import path

from . import views

urlpatterns = [
    path('my-payments', views.my_payments, name='payment.my_payments'),
]
