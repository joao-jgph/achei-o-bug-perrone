from django import forms

class MarcaImportForm(forms.Form):
	st_nome = forms.CharField(
		label='Marca (nome ou parte do nome)',
		max_length=100,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Fiat, Volkswagen'})
	)


from .models import Veiculo


class VeiculoForm(forms.ModelForm):
	class Meta:
		model = Veiculo
		fields = ['st_placa', 'fk_marca', 'fk_modelo', 'st_cor', 'dt_ano_fabricacao', 'dt_ano_modelo']
		widgets = {
			'st_placa': forms.TextInput(attrs={'class': 'form-control'}),
			'fk_marca': forms.Select(attrs={'class': 'form-control'}),
			'fk_modelo': forms.Select(attrs={'class': 'form-control'}),
			'st_cor': forms.TextInput(attrs={'class': 'form-control'}),
			'dt_ano_fabricacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'dt_ano_modelo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
		}
