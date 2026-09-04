from django import forms
import datetime

class MarcaImportForm(forms.Form):
	st_nome = forms.CharField(
		label='Marca (nome ou parte do nome)',
		max_length=100,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Fiat, Volkswagen'})
	)


from .models import Veiculo


class VeiculoForm(forms.ModelForm):
	# gerar escolhas de ano do ano atual até 1900
	_current_year = datetime.date.today().year
	YEAR_CHOICES = [(y, y) for y in range(_current_year + 1, 1899, -1)]

	dt_ano_fabricacao = forms.ChoiceField(
		choices=YEAR_CHOICES,
		widget=forms.Select(attrs={'class': 'form-control'}),
		label='Ano de Fabricação'
	)

	dt_ano_modelo = forms.ChoiceField(
		choices=YEAR_CHOICES,
		widget=forms.Select(attrs={'class': 'form-control'}),
		label='Ano do Modelo'
	)

	class Meta:
		model = Veiculo
		fields = ['st_placa', 'fk_marca', 'fk_modelo', 'st_cor', 'dt_ano_fabricacao', 'dt_ano_modelo']
		widgets = {
			'st_placa': forms.TextInput(attrs={'class': 'form-control'}),
			'fk_marca': forms.Select(attrs={'class': 'form-control'}),
			'fk_modelo': forms.Select(attrs={'class': 'form-control'}),
			'st_cor': forms.TextInput(attrs={'class': 'form-control'}),
		}
