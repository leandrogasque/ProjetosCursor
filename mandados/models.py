from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def foto_upload_path(instance, filename):
    # Gera um caminho único para cada foto baseado no ID do mandado
    return f'mandados/fotos/{instance.mandado.id}/{filename}'

class Mandado(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('cumprido', 'Cumprido'),
        ('cancelado', 'Cancelado'),
    ]

    numero_processo = models.CharField(max_length=20, unique=True)
    nome_infrator = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    crime = models.CharField(max_length=200)
    data_expedicao = models.DateField()
    data_validade = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    observacoes = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    registrado_por = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Mandado'
        verbose_name_plural = 'Mandados'
        ordering = ['-data_registro']

    def __str__(self):
        return f'Mandado #{self.numero_processo} - {self.nome_infrator}'

class Foto(models.Model):
    mandado = models.ForeignKey(Mandado, on_delete=models.CASCADE, related_name='fotos')
    arquivo = models.ImageField(upload_to=foto_upload_path)
    descricao = models.CharField(max_length=200, blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        ordering = ['-data_upload']

    def __str__(self):
        return f'Foto de {self.mandado.nome_infrator} - {self.data_upload.strftime("%d/%m/%Y %H:%M")}'
