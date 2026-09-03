from django.contrib import admin
from django.urls import path, include
from veiculos import views as veiculos_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pessoas.urls')),
    path('', include('veiculos.urls')),
]
