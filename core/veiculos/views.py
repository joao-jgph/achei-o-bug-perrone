from django.db.models import Q
from django.shortcuts import render

from .models import Categoria, Marca, Veiculo


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