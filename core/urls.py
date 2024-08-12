from django.contrib import admin #IMPORTA O MODULO ADMIN
from django.urls import path, include # 
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', include('accounts.urls')),
    path('coin/', include('coin.urls')),
    path('investments/', include('investments.urls')),
    path('wallet/', include('wallet.urls')),
    path('', include('myapp.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #