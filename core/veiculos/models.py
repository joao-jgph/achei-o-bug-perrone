from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Marca(models.Model):
    pk_id = models.AutoField(primary_key=True)
    st_nome = models.CharField(max_length=100, unique=True, verbose_name='Marca')

    def __str__(self):
        return self.st_nome

    class Meta:
        db_table = 'tb_acheiobug_marca'
class Categoria(models.Model):
    pk_id = models.AutoField(primary_key=True)
    st_nome = models.CharField(max_length=100, unique=True, verbose_name='Categoria')

    def __str__(self):
        return self.st_nome

    class Meta:
        db_table = 'tb_acheiobug_categoria'

class Modelo(models.Model):
    pk_id = models.AutoField(primary_key=True)
    st_nome = models.CharField(max_length=100, verbose_name='Modelo')
    fk_marca = models.ForeignKey('Marca', on_delete=models.PROTECT, verbose_name='Marca')

    def __str__(self):
        return self.st_nome

    class Meta:
        db_table = 'tb_acheiobug_modelo'
        constraints = [models.UniqueConstraint(fields=['st_nome', 'fk_marca'],name='unique_modelo_marca')]

class Veiculo(models.Model):
    pk_id = models.AutoField(primary_key=True)
    st_placa = models.CharField(max_length=7, unique=True, verbose_name='Placa')
    fk_marca = models.ForeignKey('Marca', on_delete=models.PROTECT, verbose_name='Marca')
    fk_modelo = models.ForeignKey('Modelo', on_delete=models.PROTECT, verbose_name='Modelo')
    st_cor = models.CharField(max_length=20, verbose_name='Cor')
    # armazenar apenas o ano como inteiro para evitar escolher dia/mês
    current_year = datetime.date.today().year
    dt_ano_fabricacao = models.PositiveSmallIntegerField(
        verbose_name='Ano de Fabricação',
        validators=[MinValueValidator(1886), MaxValueValidator(current_year + 1)],
    )
    dt_ano_modelo = models.PositiveSmallIntegerField(
        verbose_name='Ano do Modelo',
        validators=[MinValueValidator(1886), MaxValueValidator(current_year + 1)],
    )

    def __str__(self):
        return self.st_placa

    class Meta:
        db_table = 'tb_acheiobug_veiculo'

    def clean(self):
        # garante que o modelo pertence à marca selecionada
        if self.fk_modelo and self.fk_marca:
            if getattr(self.fk_modelo, 'fk_marca_id', None) != getattr(self.fk_marca, 'pk_id', None):
                raise ValidationError({'fk_modelo': 'O modelo selecionado não pertence à marca informada.'})

    def save(self, *args, **kwargs):
        # chama validação antes de salvar para evitar inconsistências
        self.full_clean()
        super().save(*args, **kwargs)



