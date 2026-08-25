from django.contrib import admin
from .models import Orgao, Usuario, UsuarioInterno, UsuarioRoot

admin.site.register(Orgao)
admin.site.register(Usuario)
admin.site.register(UsuarioInterno)
admin.site.register(UsuarioRoot)