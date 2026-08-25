from django.http import request
from django.shortcuts import render
from .forms import UsuarioInternoForm
from .models import Orgao
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect

def index(request):
    return render(request, 'pessoas/index.html')

def cadastro_interno(request):

    form = UsuarioInternoForm()

    if request.method == 'POST':

            form = UsuarioInternoForm(request.POST, request.FILES)

            if form.is_valid():

                user = User.objects.create_user(
                    username = form.cleaned_data['login'],
                    password = form.cleaned_data['senha'],
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['nome'],
                    last_name = form.cleaned_data['sobrenome'],
                )


                user.save()

                group = Group.objects.get(id=1)

                orgao = Orgao.objects.get(pk_id=form.cleaned_data['fk_orgao'])

                cadastrar_usuario_interno = form.save(commit=False)

                cadastrar_usuario_interno.fk_user = user
                cadastrar_usuario_interno.fk_group = group
                cadastrar_usuario_interno.fk_orgao = orgao

                return HttpResponseRedirect('/')

    content = { 'form' : form }

    return render (request, 'pessoas/cadastro_interno.html', content )