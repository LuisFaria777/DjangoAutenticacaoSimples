from django.shortcuts import render, redirect
from .models import InvestmentPlan, Investment, CollectiveInvestmentGroup, Redemption
from wallet.models import Wallet
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

@login_required
def view_plans(request):
    plans = InvestmentPlan.objects.all()
    return render(request, 'investments/view_plans.html', {'plans': plans})

@login_required
def create_investment(request, plan_id):
    plan = InvestmentPlan.objects.get(id=plan_id)
    wallet = Wallet.objects.get(user=request.user)  # Obtenha a carteira do usuário
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        if amount < plan.min_investment:
            messages.error(request, "O valor do investimento é menor que o mínimo permitido.")
            return redirect('investment_failed')
        if wallet.coin_balance < amount:  # Verifique se o usuário tem fundos suficientes
            messages.error(request, "Você não tem saldo suficiente para realizar esse investimento.")
            return redirect('investment_failed')

        try:
            # Debitar moedas da carteira do usuário
            wallet.withdraw_coins(amount)
            
            # Criar o investimento
            end_date = timezone.now().date() + timedelta(days=plan.duration_days)
            investment = Investment(user=request.user, plan=plan, amount=amount, end_date=end_date)
            investment.save()
            messages.success(request, "Investimento realizado com sucesso!")
            return redirect('investment_success')
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao processar o investimento: {str(e)}")
            return redirect('investment_failed')
    
    return render(request, 'investments/create_investment.html', {'plan': plan})


@login_required
def join_collective_investment(request, plan_id):
    plan = InvestmentPlan.objects.get(id=plan_id)
    group, created = CollectiveInvestmentGroup.objects.get_or_create(plan=plan, end_date=timezone.now().date() + timedelta(days=plan.duration_days))
    wallet = Wallet.objects.get(user=request.user)  # Obtenha a carteira do usuário
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        if wallet.coin_balance < amount:  # Verifique se o usuário tem fundos suficientes
            return redirect('insufficient_funds')

        # Debitar moedas da carteira do usuário
        wallet.withdraw_coins(amount)
        
        group.members.add(request.user)
        group.total_investment += amount
        group.save()
        return redirect('investment_success')
    return render(request, 'investments/join_collective_investment.html', {'plan': plan, 'group': group})

@login_required
def view_investments(request):
    investments = Investment.objects.filter(user=request.user, is_active=True)
    return render(request, 'investments/view_investments.html', {'investments': investments})

@login_required
def redeem_investment(request, investment_id):
    investment = Investment.objects.get(id=investment_id, user=request.user)
    wallet = Wallet.objects.get(user=request.user)
    if investment.check_completion():
        # Resgatar fundos com juros
        total_redeemable = investment.amount + investment.interest_earned
        wallet.deposit_coins(total_redeemable)
        Redemption.objects.create(investment=investment, redeemed_amount=total_redeemable)
        return redirect('redemption_success')
    return redirect('redemption_failed')

@login_required
def investment_success(request):
    return render(request, 'investments/investment_success.html')

@login_required
def investment_failed(request):
    return render(request, 'investments/investment_failed.html')