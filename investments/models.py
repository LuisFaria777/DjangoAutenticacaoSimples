from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from wallet.models import Wallet

# Modelos para os Planos de Investimento
class InvestmentPlan(models.Model):
    PLAN_TYPES = [
        ('individual', 'Individual'),
        ('collective', 'Coletivo'),
    ]
    name = models.CharField(max_length=100)
    duration_days = models.IntegerField()  # Duração do plano em dias
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Taxa de retorno
    min_investment = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)  # Investimento mínimo
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPES, default='individual')

    def __str__(self):
        return self.name

class Investment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    interest_earned = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    
    def calculate_return(self):
        return self.amount * (1 + self.plan.interest_rate / 100)
    
    def check_completion(self):
        if timezone.now().date() >= self.end_date:
            self.is_active = False
            self.interest_earned = self.calculate_return() - self.amount
            self.save()
            return True
        return False

    def withdraw(self):
        # Retorno somente se o plano foi completado, caso contrário, aplicar regras de penalidade
        if self.is_active and timezone.now().date() >= self.end_date:
            self.is_active = False
            return self.calculate_return()
        else:
            return self.amount  # No caso de desistência, retornar apenas o valor investido

class CollectiveInvestmentGroup(models.Model):
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser)
    total_investment = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def calculate_return(self):
        base_return = self.total_investment * (1 + self.plan.interest_rate / 100)
        bonus = 0.5 if self.members.count() == 5 else 1.0 if self.members.count() == 10 else 0.0
        return base_return * (1 + bonus / 100)

class Redemption(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    redeemed_amount = models.DecimalField(max_digits=20, decimal_places=2)
    redemption_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resgate de {self.investment.user.username} - {self.redeemed_amount} Moedas Paradise"
