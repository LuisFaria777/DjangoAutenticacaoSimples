from django.shortcuts import render
from .models import ParadiseCoin
from django.http import JsonResponse

def generate_coins(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        coin = ParadiseCoin.objects.first()
        if coin.issue_coins(amount):
            return JsonResponse({'status': 'success', 'message': f'{amount} coins issued successfully.'})
        return JsonResponse({'status': 'failed', 'message': 'Failed to issue coins.'})
    return render(request, 'coin/generate_coins.html')

def convert_coins(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        coin = ParadiseCoin.objects.first()
        brl_amount = coin.convert_to_brl(amount)
        if brl_amount:
            return JsonResponse({'status': 'success', 'brl_amount': brl_amount})
        return JsonResponse({'status': 'failed', 'message': 'Conversion failed.'})
    return render(request, 'coin/convert_coins.html')
