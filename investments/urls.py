from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.view_plans, name='view_plans'),
    path('invest/<int:plan_id>/', views.create_investment, name='create_investment'),
    path('my_investments/', views.view_investments, name='view_investments'),
    path('redeem/<int:investment_id>/', views.redeem_investment, name='redeem_investment'),
    path('success/', views.investment_success, name='investment_success'),
    path('failed/', views.investment_failed, name='investment_failed'),
]
