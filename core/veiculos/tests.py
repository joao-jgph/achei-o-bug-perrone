from django.test import TestCase
from django.urls import reverse

from .models import Marca, Modelo, Veiculo


class FrotaViewTests(TestCase):
    def test_frota_exibe_veiculos_cadastrados(self):
        marca = Marca.objects.create(st_nome='Fiat')
        modelo = Modelo.objects.create(st_nome='Uno', fk_marca=marca)
        Veiculo.objects.create(
            st_placa='ABC1234',
            fk_marca=marca,
            fk_modelo=modelo,
            st_cor='Vermelho',
            dt_ano_fabricacao='2020-01-01',
            dt_ano_modelo='2020-01-01',
        )

        response = self.client.get(reverse('veiculos:frota'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ABC1234')
        self.assertContains(response, 'Fiat')
        self.assertContains(response, 'Uno')
