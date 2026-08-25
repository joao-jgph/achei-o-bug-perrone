from django.db import models
from django.contrib.auth.models import User, Group

class Orgao(models.Model):
    pk_id = models.AutoField(primary_key=True)
    st_sigla = models.CharField(max_length=100)
    st_descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.st_sigla

    class Meta:
        db_table = 'tb_acheiobug_orgao'


class Usuario(models.Model):
    fk_user = models.OneToOneField(User, related_name='usuario', on_delete= models.PROTECT, verbose_name='User')
    fk_nivel = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='Nível')
    fk_orgao = models.ForeignKey(Orgao, related_name='Orgao', on_delete=models.PROTECT, verbose_name='Orgão')

    def __str__(self):
        return self.fk_user.username
    
    class Meta:
        db_table = 'tb_acheiobug_usuario'

class UsuarioInterno(Usuario):
    st_cpf = models.CharField(max_length=14, blank=True, unique=True, null=True, verbose_name='CPF')
    st_foto = models.ImageField(upload_to= 'uploads/imagens/%Y/%m/%d', blank=True, verbose_name='Foto')
    st_contato = models.CharField(max_length=30, blank=True, null=True, verbose_name='Contato')
    bo_questionamento_whatsapp = models.BooleanField(default=False, verbose_name='Questionamento Whatsapp')

    def __str__(self):
        return self.fk_user.username

    class Meta:
        db_table = 'tb_acheiobug_usuariointerno'

class UsuarioRoot(Usuario):
    st_anexo_comprovante_autorizacao = models.FileField(upload_to= 'uploads/anexos/%Y/%m/%d/', verbose_name='Anexo comprovante de autorização')

    def __str__(self):
        return self.fk_user.username
    
    class Meta:
        db_table = 'tb_acheiobug_usuarioroot'