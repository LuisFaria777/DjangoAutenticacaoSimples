from django.contrib import admin
from .models import InvestmentPlan, Investment, CollectiveInvestmentGroup

@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_days', 'interest_rate', 'min_investment', 'plan_type')

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'start_date', 'end_date', 'is_active')

@admin.register(CollectiveInvestmentGroup)
class CollectiveInvestmentGroupAdmin(admin.ModelAdmin):
    list_display = ('plan', 'total_investment', 'start_date', 'end_date')
