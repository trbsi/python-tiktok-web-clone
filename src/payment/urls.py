from django.urls import path

from . import views

urlpatterns = [
    path('my-spendings', views.my_spendings, name='payment.my_spendings'),
    path('list-packages', views.list_packages, name='payment.list_packages'),
    path('buy-package/<int:package_id>', views.buy_single_package, name='payment.buy_single_package'),

    path('api/balance', views.api_get_balance, name='payment.api.get_balance'),
    path('api/can-purchase', views.api_can_purchase, name='payment.can_purchase'),
]
