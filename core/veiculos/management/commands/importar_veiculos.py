import requests

from django.core.management.base import BaseCommand
from veiculos.models import Marca, Modelo


class Command(BaseCommand):
    help = 'Importa marcas e modelos de veículos'

    def handle(self, *args, **kwargs):

        url_marcas = 'https://parallelum.com.br/fipe/api/v1/carros/marcas'

        self.stdout.write('Buscando marcas...')

        resposta = requests.get(url_marcas)

        if resposta.status_code != 200:
            self.stdout.write(
                self.style.ERROR('Erro ao buscar marcas.')
            )
            return

        marcas = resposta.json()

        total_marcas = 0
        total_modelos = 0

        for marca in marcas:

            marca_obj, criada = Marca.objects.get_or_create(
                st_nome=marca['nome']
            )

            if criada:
                total_marcas += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Marca criada: {marca["nome"]}'
                    )
                )

            url_modelos = (
                f'https://parallelum.com.br/fipe/api/v1/carros/marcas/'
                f'{marca["codigo"]}/modelos'
            )

            resposta_modelos = requests.get(url_modelos)

            if resposta_modelos.status_code != 200:
                self.stdout.write(
                    self.style.WARNING(
                        f'Não foi possível buscar modelos de '
                        f'{marca["nome"]}'
                    )
                )
                continue

            modelos = resposta_modelos.json()['modelos']

            for modelo in modelos:

                nome_modelo = modelo['nome']

                modelo_obj, criado = Modelo.objects.get_or_create(
                    st_nome=nome_modelo,
                    defaults={
                        'fk_marca': marca_obj
                    }
                )

                if criado:
                    total_modelos += 1

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                'Importação concluída!'
            )
        )

        self.stdout.write(
            f'Marcas novas: {total_marcas}'
        )

        self.stdout.write(
            f'Modelos novos: {total_modelos}'
        )