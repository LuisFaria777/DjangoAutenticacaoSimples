from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_coins, name='generate_coins'),
    path('convert/', views.convert_coins, name='convert_coins'),
]
