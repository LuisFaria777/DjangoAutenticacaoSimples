from django.db import models
from accounts.models import CustomUser

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    coin_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    brl_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def deposit_coins(self, amount):
        self.coin_balance += amount
        self.save()

    def withdraw_coins(self, amount):
        if amount <= self.coin_balance:
            self.coin_balance -= amount
            self.save()
            return True
        return False

    def deposit_brl(self, amount):
        self.brl_balance += amount
        self.save()

    def withdraw_brl(self, amount):
        if amount <= self.brl_balance:
            self.brl_balance -= amount
            self.save()
            return True
        return False

    def __str__(self):
        return f'Carteira de {self.user.username} - Moedas: {self.coin_balance}, BRL: {self.brl_balance}'
    
class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount_brl = models.DecimalField(max_digits=20, decimal_places=2)  # Valor em BRL
    coins_acquired = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Converter BRL para Moedas Paradise e adicionar à carteira do usuário
        exchange_rate = 1  # Exemplo: 1 BRL = 5 Moedas Paradise
        self.coins_acquired = self.amount_brl * exchange_rate
        wallet, created = Wallet.objects.get_or_create(user=self.user)
        wallet.deposit(self.coins_acquired)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Compra de {self.coins_acquired} Moedas Paradise por {self.user.username} em {self.date}'
    
class CoinPackage(models.Model):
    coins = models.IntegerField()  # Quantidade de moedas no pacote
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço em reais

    def __str__(self):
        return f"{self.coins} moedas - R${self.price}"
