from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet_details, name='wallet_details'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('convert/', views.convert_to_brl, name='convert_to_brl'),
    path('wallet/', views.wallet_details, name='wallet_details'),
    path('purchase/confirm/', views.confirm_purchase, name='confirm_purchase'),
    path('purchase/success/', views.purchase_success, name='purchase_success'),
    path('convert/', views.convert_to_brl, name='convert_to_brl'),
    path('coin-packages/', views.coin_packages, name='coin_packages'),
    path('purchase/<int:package_id>/', views.purchase_coins, name='purchase_coins'),
]
