from django.db import models

class ParadiseCoin(models.Model):
    total_supply = models.DecimalField(max_digits=20, decimal_places=2, default=1000000.00)
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)

    def issue_coins(self, amount):
        if self.circulating_supply + amount <= self.total_supply:
            self.circulating_supply += amount
            return True
        return False

    def convert_to_brl(self, coins):
        return coins * self.exchange_rate if coins <= self.circulating_supply else None