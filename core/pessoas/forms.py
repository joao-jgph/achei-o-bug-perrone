from django import forms
from django.forms import ModelForm
from .models import UsuarioInterno
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row
from crispy_forms.bootstrap import Field, StrictButton

class UsuarioInternoForm(ModelForm):
    login = forms.CharField(max_length=100)
    nome = forms.CharField(max_length=100)
    sobrenome = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    senha = forms.CharField(max_length=100, widget= forms.PasswordInput(attrs= { 'class' : "form-control"}))
    lgpd = forms.BooleanField(required=True, label= 'Concrodo com a coleta e tratamento dos meus dados pessoais segundo o que estabelece a LGPD')

    class Meta:
        model = UsuarioInterno
        exclude = [
            'fk_nivel',
            'fk_user'
        ]

    def __init__(self, *args, **kwargs):
        super(UsuarioInternoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.fields['fk_orgao'].empty_label = 'Selecione Aqui'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(Field('nome'), css_class='col-md-4'),
                Column(Field('sobrenome'), css_class='col-md-4'),
                Column(Field('login'), css_class='col-md-4'),
            ),
            Row(
                Column(Field('email'), css_class='col-md-5'),
                Column(Field('senha'), css_class='col-md-4'),
            ),            
            Row(
                Column(Field('st_contato'), css_class='col-md-4'),
                Column(Field('bo_questionamento_whatsapp'), css_class='col-md-4'),
            ),
            Row(
                Column(Field('fk_orgao'), css_class='col-md-4'),
                Column(Field('st_cpf'), css_class='col-md-4'),
                Column(Field('st_foto'), css_class='col-md-4'),
            ),

            Row(
                Column(Field('lgpd'), css_class='col-md-12'),
            ),
            Row(
                Column(
                    StrictButton(
                            "Cadastrar",
                            type='submit',
                            css_class='btn-default btn-primary col-md-offset-8 teste-submit-form' 
                    ),
                ),
            ),
        )