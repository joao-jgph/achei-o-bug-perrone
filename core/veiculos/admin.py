from django.contrib import admin
from .models import Veiculo, Marca, Modelo, Categoria

admin.site.register(Veiculo)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Categoria)