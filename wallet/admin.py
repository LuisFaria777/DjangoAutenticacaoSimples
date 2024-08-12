from django.contrib import admin
from .models import Wallet, Purchase, CoinPackage

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin_balance', 'brl_balance')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_brl', 'coins_acquired', 'date')
    search_fields = ('user__username',)

@admin.register(CoinPackage)
class CoinPackageAdmin(admin.ModelAdmin):
    list_display = ('coins', 'price')
