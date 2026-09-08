from django.contrib import messages
from django.shortcuts import render
from .forms import UsuarioInternoForm
from .models import Orgao, UsuarioInterno
from django.contrib.auth.models import Group, User
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.conf import settings
import logging
import smtplib

logger = logging.getLogger('db')

def index(request):
    return render(request, 'pessoas/index.html')


def cadastro_interno(request):

    form = UsuarioInternoForm()

    if request.method == 'POST':

        form = UsuarioInternoForm(request.POST, request.FILES)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['senha'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['nome'],
                last_name=form.cleaned_data['sobrenome'],
            )

            nivel = Group.objects.get(id=1)

            orgao = form.cleaned_data['fk_orgao']

            cadastrar_usuario_interno = form.save(commit=False)

            cadastrar_usuario_interno.fk_user = user
            cadastrar_usuario_interno.fk_orgao = orgao
            cadastrar_usuario_interno.fk_nivel = nivel

            cadastrar_usuario_interno.save()

            logger.info(f'Novo login: "{user.username}" criado. ')

            try:
                email_body = f"""
                <html>
                    <body>
                        <h2>AVISOS ACHEI O BUG</h2>
                        <p>Olá {form.cleaned_data['nome']} {form.cleaned_data['sobrenome']},</p>
                        <p>Seu cadastro foi realizado com sucesso!</p>
                    </body>
                </html>
                """

                email = EmailMessage(
                    subject='Cadastro realizado com sucesso!',
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[form.cleaned_data['email']]
                )
                email.content_subtype = 'html'
                email.send(fail_silently=False)

            except (OSError, smtplib.SMTPException):
                logger.exception('Falha ao enviar e-mail de confirmação para %s', form.cleaned_data['email'])
                messages.error(
                    request,
                    'Erro ao enviar o e-mail de confirmação. Por favor, verifique o endereço de e-mail fornecido.'
                )

            messages.success(
                request,
                'Usuário cadastrado com sucesso!'
            )

            return HttpResponseRedirect('/')

    content = {'form': form}

    return render(
        request,
        'pessoas/cadastro_interno.html',
        content
    )

def atualizar_cadastro_interno(request, user_id=None):

    uid = user_id or (request.user.id if request.user.is_authenticated else None)
    if not uid:
        messages.error(request, 'Usuário não autenticado.')
        return HttpResponseRedirect('/')

    try:
        usuario_interno = UsuarioInterno.objects.get(fk_user__id=uid)
    except UsuarioInterno.DoesNotExist:
        messages.error(request, 'Cadastro interno não encontrado para este usuário.')
        return HttpResponseRedirect('/')

    form = UsuarioInternoForm(instance=usuario_interno)

    if request.method == 'POST':

         form = UsuarioInternoForm(request.POST, instance=usuario_interno)

    if form.is_valid():

        usuario = User.objects.get(id=request.user.id)
        usuario.email = form.cleaned_data['email']
        usuario.first_name = form.cleaned_data['nome']
        usuario.last_name = form.cleaned_data['sobrenome']
        usuario.username = form.cleaned_data['login']
        usuario.set_password(form.cleaned_data['senha'])
        usuario.save()
        update_session_auth_hash(request, usuario)
        print(usuario.email)

        form.save()

        try:
            email_body = f"""\
            <html>
            <head></head>
            <body>
                <h2>STATUS ACHEI O BUG</h2>
                <p>Seu cadastro foi atualizado com sucesso!!</p>
                <p>Para mais informações entrar em contato com a SEMIT</p>
            </body>
            </html>
            """
            email = EmailMessage('Achei O Bug', email_body, to=[usuario.email])
            email.content_subtype = "html" # this is the crucial part
            email.send()
        except:
            messages.error(request, "Falha ao enviar email!")

            logger.info('Cadastro Interno Atualizado', extra={'user': request.user.username })

            messages.success(request, "Cadastro atualizado com sucesso!")

    context = {
        'form': form,
    }
    
    return render(request, 'pessoas/atualizar_cadastro_interno.html', context)