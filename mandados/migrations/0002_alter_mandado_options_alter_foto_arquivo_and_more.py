# Generated by Django 5.2 on 2025-04-04 02:25

import mandados.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandados', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mandado',
            options={'ordering': ['-data_registro'], 'verbose_name': 'Mandado', 'verbose_name_plural': 'Mandados'},
        ),
        migrations.AlterField(
            model_name='foto',
            name='arquivo',
            field=models.ImageField(upload_to=mandados.models.foto_upload_path),
        ),
        migrations.AlterField(
            model_name='foto',
            name='data_upload',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='mandado',
            name='data_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='mandado',
            name='numero_processo',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='mandado',
            name='registrado_por',
            field=models.CharField(max_length=100),
        ),
    ]
