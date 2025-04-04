from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
import os

def foto_upload_path(instance, filename):
    # Gera um caminho único para cada foto baseado no ID do mandado
    return f'mandados/fotos/{instance.mandado.id}/{filename}'

class Mandado(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('executado', 'Executado'),
        ('cancelado', 'Cancelado'),
        ('expirado', 'Expirado'),
    ]

    numero_processo = models.CharField(max_length=50, unique=True)
    nome_infrator = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    cpf = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF deve estar no formato: 000.000.000-00'
            )
        ]
    )
    rg = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=200, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    crime = models.CharField(max_length=200)
    data_expedicao = models.DateField()
    data_validade = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    observacoes = models.TextField(blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    registrado_por = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Mandado'
        verbose_name_plural = 'Mandados'
        ordering = ['-data_expedicao']

    def __str__(self):
        return f'{self.numero_processo} - {self.nome_infrator}'

    def get_pdf_path(self):
        """Retorna o caminho do PDF do mandado"""
        pdf_dir = f'mandados/pdfs/{self.pk}'
        if not os.path.exists(pdf_dir):
            return None
        
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        if not pdf_files:
            return None
        
        return os.path.join(pdf_dir, pdf_files[0])
    
    def get_fotos(self):
        """Retorna o caminho das fotos do mandado"""
        fotos_dir = f'mandados/fotos/{self.pk}'
        if not os.path.exists(fotos_dir):
            return []
        
        return [os.path.join(fotos_dir, f) for f in os.listdir(fotos_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

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
