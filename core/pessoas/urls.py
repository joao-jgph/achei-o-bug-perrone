from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'pessoas'

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro-interno', views.cadastro_interno, name='cadastro_interno'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout-logged-out/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logged_out'),
        path('atualizar-cadastro-interno/', views.atualizar_cadastro_interno, name='atualizar_cadastro_interno'),
        path('atualizar-cadastro-interno/<int:user_id>/', views.atualizar_cadastro_interno, name='atualizar_cadastro_interno_with_id'),
]
