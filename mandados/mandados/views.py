from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Mandado, Foto
from .utils import extract_mandado_data
from .forms import MandadoForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

# Create your views here.

@login_required
def listar_mandados(request):
    mandados = Mandado.objects.all().order_by('-data_expedicao')
    return render(request, 'mandados/listar.html', {'mandados': mandados})

@login_required
def novo_mandado(request):
    if request.method == 'POST':
        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            try:
                # Extrair dados do PDF
                dados = extract_mandado_data(pdf_file)
                
                # Verificar se já existe um mandado com o mesmo número de processo
                if Mandado.objects.filter(numero_processo=dados['numero_processo']).exists():
                    mandado_existente = Mandado.objects.get(numero_processo=dados['numero_processo'])
                    messages.warning(request, f'Já existe um mandado com o número de processo {dados["numero_processo"]}.')
                    return redirect('mandados:visualizar', pk=mandado_existente.pk)
                
                # Criar o mandado com os dados extraídos
                mandado = Mandado.objects.create(**dados)
                
                # Salvar o arquivo PDF
                pdf_path = f'mandados/pdfs/{mandado.pk}/{pdf_file.name}'
                default_storage.save(pdf_path, ContentFile(pdf_file.read()))
                
                # Salvar as fotos se houver
                if 'fotos' in request.FILES:
                    for foto in request.FILES.getlist('fotos'):
                        foto_path = f'mandados/fotos/{mandado.pk}/{foto.name}'
                        default_storage.save(foto_path, ContentFile(foto.read()))
                
                messages.success(request, 'Mandado criado com sucesso!')
                return redirect('mandados:visualizar', pk=mandado.pk)
                
            except Exception as e:
                messages.error(request, f'Erro ao processar o PDF: {str(e)}')
                return redirect('mandados:novo')
        else:
            form = MandadoForm(request.POST)
            if form.is_valid():
                mandado = form.save()
                
                # Salvar as fotos se houver
                if 'fotos' in request.FILES:
                    for foto in request.FILES.getlist('fotos'):
                        foto_path = f'mandados/fotos/{mandado.pk}/{foto.name}'
                        default_storage.save(foto_path, ContentFile(foto.read()))
                
                messages.success(request, 'Mandado criado com sucesso!')
                return redirect('mandados:visualizar', pk=mandado.pk)
    else:
        form = MandadoForm()
    
    return render(request, 'mandados/form.html', {'form': form})

@login_required
def visualizar_mandado(request, pk):
    mandado = get_object_or_404(Mandado, pk=pk)
    return render(request, 'mandados/visualizar.html', {'mandado': mandado})

@login_required
def editar_mandado(request, pk):
    mandado = get_object_or_404(Mandado, pk=pk)
    
    if request.method == 'POST':
        form = MandadoForm(request.POST, instance=mandado)
        if form.is_valid():
            mandado = form.save()
            messages.success(request, 'Mandado atualizado com sucesso!')
            return redirect('mandados:visualizar', pk=mandado.pk)
    else:
        form = MandadoForm(instance=mandado)
    
    return render(request, 'mandados/form.html', {'form': form, 'mandado': mandado})

@login_required
def excluir_mandado(request, pk):
    mandado = get_object_or_404(Mandado, pk=pk)
    
    # Excluir arquivos associados
    pdf_dir = f'mandados/pdfs/{pk}'
    fotos_dir = f'mandados/fotos/{pk}'
    
    if default_storage.exists(pdf_dir):
        default_storage.delete(pdf_dir)
    
    if default_storage.exists(fotos_dir):
        default_storage.delete(fotos_dir)
    
    mandado.delete()
    messages.success(request, 'Mandado excluído com sucesso!')
    return redirect('mandados:listar')

@login_required
def carrossel_fotos(request):
    # Buscar todas as fotos de mandados ativos, ordenadas por data de upload
    fotos = Foto.objects.filter(
        mandado__status='ativo'
    ).select_related('mandado').order_by('-data_upload')
    
    return render(request, 'mandados/carrossel.html', {'fotos': fotos})
