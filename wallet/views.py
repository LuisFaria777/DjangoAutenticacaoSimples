from django.shortcuts import render, redirect
from .models import Wallet, Purchase, CoinPackage
from django.contrib.auth.decorators import login_required
from coin.models import ParadiseCoin

#@login_required
def wallet_details(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)  # Garantir que a carteira existe
    return render(request, 'wallet/wallet_details.html', {'wallet': wallet})

@login_required
def convert_to_brl(request):
    wallet = Wallet.objects.get(user=request.user)
    coin = ParadiseCoin.objects.first()
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        brl_amount = wallet.convert_to_brl(coin, amount)
        if brl_amount:
            return redirect('conversion_success')
        return redirect('conversion_failed')
    return render(request, 'wallet/convert_to_brl.html', {'wallet': wallet})

@login_required
def purchase_coins(request, package_id):
    package = CoinPackage.objects.get(id=package_id)
    wallet = Wallet.objects.get(user=request.user)
    wallet.coin_balance += package.coins
    wallet.save()
    
    return redirect('wallet_details')
    
@login_required
def convert_to_brl(request):
    wallet = Wallet.objects.get(user=request.user)
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        if wallet.withdraw_coins(amount):
            exchange_rate = 5  # Exemplo: 1 Moeda Paradise = 5 BRL
            brl_amount = amount * exchange_rate
            wallet.deposit_brl(brl_amount)
            return redirect('wallet_details')
        else:
            # Adicione uma mensagem de erro aqui se o usuário não tiver saldo suficiente em Moedas Paradise
            pass
    return render(request, 'wallet/convert_to_brl.html')


@login_required
def confirm_purchase(request):
    purchase_details = request.session.get('purchase_details')
    if request.method == 'POST':
        amount_coins = purchase_details['amount_coins']
        amount_brl = purchase_details['amount_brl']

        # Simular o processo de pagamento via PIX
        # Após o pagamento ser bem-sucedido, registrar a compra
        purchase = Purchase(user=request.user, amount_brl=amount_brl)
        purchase.save()

        # Atualizar o saldo de moedas do usuário
        wallet = Wallet.objects.get(user=request.user)
        wallet.deposit_coins(amount_coins)
        
        # Limpar os detalhes da compra da sessão
        del request.session['purchase_details']

        return redirect('purchase_success')
    
    return render(request, 'wallet/confirm_purchase.html', {'purchase_details': purchase_details})

@login_required
def purchase_success(request):
    return render(request, 'wallet/purchase_success.html')

@login_required
def coin_packages(request):
    packages = CoinPackage.objects.all()
    return render(request, 'wallet/coin_packages.html', {'packages': packages})