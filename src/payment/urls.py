from django.urls import path

from . import views

urlpatterns = [
    path('my-spendings', views.my_spendings, name='payment.my_spendings'),
    path('api/balance', views.api_get_balance, name='payment.api.get_balance'),
    path('buy-packages', views.buy_packages, name='payment.buy_packages'),
]
