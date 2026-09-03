from django.contrib import admin
from django import forms
from .models import Veiculo, Marca, Modelo, Categoria


class VeiculoAdminForm(forms.ModelForm):
	class Meta:
		model = Veiculo
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Se a marca já estiver selecionada (edição) ou enviada via POST, limitar os modelos
		marca_id = None
		if self.instance and getattr(self.instance, 'fk_marca', None):
			marca_id = getattr(self.instance.fk_marca, 'pk_id', None)
		else:
			data = getattr(self, 'data', None)
			if data and data.get('fk_marca'):
				try:
					marca_id = int(data.get('fk_marca'))
				except (TypeError, ValueError):
					marca_id = None

		if marca_id:
			self.fields['fk_modelo'].queryset = Modelo.objects.filter(fk_marca__pk_id=marca_id)


class VeiculoAdmin(admin.ModelAdmin):
	form = VeiculoAdminForm


admin.site.register(Veiculo, VeiculoAdmin)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Categoria)