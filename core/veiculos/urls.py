from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    path('frota', views.frota, name='frota'),
    path('cadastro', views.cadastro_veiculos, name='cadastro_veiculos'),
    path('importar', views.importar_marca, name='importar_marca'),
]
