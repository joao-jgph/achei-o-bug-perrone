from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    path('', views.frota, name='frota'),
    path('cadastro/', views.cadastro_veiculos, name='cadastro_veiculos'),
]
