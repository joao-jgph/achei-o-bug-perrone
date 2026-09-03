from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
import requests

from .models import Categoria, Marca, Veiculo, Modelo
from .forms import MarcaImportForm, VeiculoForm


def frota(request):
    veiculos = Veiculo.objects.select_related('fk_marca', 'fk_modelo')

    marca = request.GET.get('marca')
    if marca:
        veiculos = veiculos.filter(fk_marca__st_nome__iexact=marca)

    busca = request.GET.get('q')
    if busca:
        veiculos = veiculos.filter(
            Q(fk_marca__st_nome__icontains=busca)
            | Q(fk_modelo__st_nome__icontains=busca)
            | Q(st_placa__icontains=busca)
        )

    ordem = request.GET.get('ordem', 'marca')
    ordem_map = {
        'marca': 'fk_marca__st_nome',
        'modelo': 'fk_modelo__st_nome',
        'ano': 'dt_ano_fabricacao',
        'placa': 'st_placa',
    }
    campo_ordem = ordem_map.get(ordem, 'fk_marca__st_nome')
    direcao = request.GET.get('direcao', 'asc')

    if direcao == 'desc':
        veiculos = veiculos.order_by(f'-{campo_ordem}')
    else:
        veiculos = veiculos.order_by(campo_ordem)

    context = {
        'veiculos': veiculos,
        'marcas': Marca.objects.order_by('st_nome').values_list('st_nome', flat=True),
        'categorias': Categoria.objects.order_by('st_nome').values_list('st_nome', flat=True),
    }
    return render(request, 'veiculos/frota.html', context)

def cadastro_veiculos(request):
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    modelos = Modelo.objects.select_related('fk_marca').order_by('fk_marca__st_nome', 'st_nome')

    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo cadastrado com sucesso.')
            return redirect('veiculos:cadastro_veiculos')
        else:
            messages.error(request, 'Por favor corrija os erros no formulário.')
    else:
        form = VeiculoForm()

    context = {
        'categorias': categorias,
        'marcas': marcas,
        'modelos': modelos,
        'form': form,
    }
    return render(request, 'veiculos/cadastro_veiculos.html', context)


def importar_marca(request):
    form = MarcaImportForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        nome = form.cleaned_data['st_nome']

        url_marcas = 'https://parallelum.com.br/fipe/api/v1/carros/marcas'
        resposta = requests.get(url_marcas)

        if resposta.status_code != 200:
            messages.error(request, 'Erro ao buscar marcas na API.')
            return render(request, 'veiculos/importar_marca.html', {'form': form})

        marcas = resposta.json()

        encontrados = [m for m in marcas if nome.lower() in m['nome'].lower()]

        if not encontrados:
            messages.warning(request, f'Nenhuma marca encontrada para "{nome}".')
            return render(request, 'veiculos/importar_marca.html', {'form': form})

        total_marcas = 0
        total_modelos = 0

        for marca in encontrados:
            marca_obj, criada = Marca.objects.get_or_create(st_nome=marca['nome'])
            if criada:
                total_marcas += 1

            url_modelos = (
                f'https://parallelum.com.br/fipe/api/v1/carros/marcas/{marca["codigo"]}/modelos'
            )

            resposta_modelos = requests.get(url_modelos)

            if resposta_modelos.status_code != 200:
                messages.warning(request, f'Não foi possível buscar modelos de {marca["nome"]}.')
                continue

            modelos = resposta_modelos.json().get('modelos', [])

            for modelo in modelos:
                nome_modelo = modelo['nome']
                modelo_obj, criado = Modelo.objects.get_or_create(
                    st_nome=nome_modelo,
                    defaults={'fk_marca': marca_obj}
                )
                if criado:
                    total_modelos += 1

        messages.success(request, f'Importação concluída! Marcas novas: {total_marcas}. Modelos novos: {total_modelos}.')
        return redirect('veiculos:importar_marca')

    return render(request, 'veiculos/importar_marca.html', {'form': form})