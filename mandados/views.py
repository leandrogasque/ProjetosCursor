from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Mandado, Foto
from .utils import extract_mandado_data

# Create your views here.

@login_required
def listar_mandados(request):
    mandados = Mandado.objects.all().order_by('-data_registro')
    return render(request, 'mandados/listar.html', {'mandados': mandados})

@login_required
def novo_mandado(request):
    if request.method == 'POST':
        try:
            # Verifica se é um upload de PDF
            if 'pdf_file' in request.FILES:
                pdf_file = request.FILES['pdf_file']
                if not pdf_file.name.endswith('.pdf'):
                    raise Exception('O arquivo deve ser um PDF')
                
                try:
                    # Extrai dados do PDF
                    data = extract_mandado_data(pdf_file)
                    data['registrado_por'] = request.user.username
                    
                    # Cria o mandado
                    mandado = Mandado.objects.create(**data)
                    
                    # Salva o PDF como foto
                    Foto.objects.create(
                        mandado=mandado,
                        arquivo=pdf_file,
                        descricao='Documento original do mandado'
                    )
                    
                    messages.success(request, 'Mandado importado com sucesso do PDF!')
                    return redirect('mandados:visualizar', pk=mandado.pk)
                except Exception as e:
                    messages.error(request, f'Erro ao processar o PDF: {str(e)}')
                    return redirect('mandados:novo')
            
            # Processamento normal do formulário
            mandado = Mandado(
                numero_processo=request.POST['numero_processo'],
                nome_infrator=request.POST['nome_infrator'],
                data_nascimento=request.POST['data_nascimento'],
                cpf=request.POST['cpf'],
                rg=request.POST.get('rg', ''),
                endereco=request.POST.get('endereco', ''),
                cidade=request.POST.get('cidade', ''),
                estado=request.POST.get('estado', ''),
                crime=request.POST['crime'],
                data_expedicao=request.POST['data_expedicao'],
                data_validade=request.POST.get('data_validade', None),
                status=request.POST['status'],
                observacoes=request.POST.get('observacoes', ''),
                registrado_por=request.user.username
            )
            mandado.save()

            # Processar fotos
            fotos = request.FILES.getlist('fotos')
            for foto in fotos:
                Foto.objects.create(
                    mandado=mandado,
                    arquivo=foto,
                    descricao=foto.name
                )

            messages.success(request, 'Mandado criado com sucesso!')
            return redirect('mandados:visualizar', pk=mandado.pk)
        except Exception as e:
            messages.error(request, f'Erro ao criar mandado: {str(e)}')
            return redirect('mandados:novo')

    return render(request, 'mandados/form.html')

@login_required
def visualizar_mandado(request, pk):
    mandado = get_object_or_404(Mandado, pk=pk)
    return render(request, 'mandados/visualizar.html', {'mandado': mandado})

@login_required
def editar_mandado(request, pk):
    mandado = get_object_or_404(Mandado, pk=pk)
    if request.method == 'POST':
        try:
            mandado.numero_processo = request.POST['numero_processo']
            mandado.nome_infrator = request.POST['nome_infrator']
            mandado.data_nascimento = request.POST['data_nascimento']
            mandado.cpf = request.POST['cpf']
            mandado.rg = request.POST.get('rg', '')
            mandado.endereco = request.POST.get('endereco', '')
            mandado.cidade = request.POST.get('cidade', '')
            mandado.estado = request.POST.get('estado', '')
            mandado.crime = request.POST['crime']
            mandado.data_expedicao = request.POST['data_expedicao']
            mandado.data_validade = request.POST.get('data_validade', None)
            mandado.status = request.POST['status']
            mandado.observacoes = request.POST.get('observacoes', '')
            mandado.data_atualizacao = timezone.now()
            mandado.save()

            # Processar novas fotos
            fotos = request.FILES.getlist('fotos')
            for foto in fotos:
                Foto.objects.create(
                    mandado=mandado,
                    arquivo=foto,
                    descricao=foto.name
                )

            messages.success(request, 'Mandado atualizado com sucesso!')
            return redirect('mandados:visualizar', pk=mandado.pk)
        except Exception as e:
            messages.error(request, f'Erro ao atualizar mandado: {str(e)}')
            return redirect('mandados:editar', pk=pk)

    return render(request, 'mandados/form.html', {'mandado': mandado})

@login_required
def excluir_mandado(request, pk):
    mandado = get_object_or_404(Mandado, pk=pk)
    if request.method == 'POST':
        try:
            mandado.delete()
            messages.success(request, 'Mandado excluído com sucesso!')
            return redirect('mandados:listar')
        except Exception as e:
            messages.error(request, f'Erro ao excluir mandado: {str(e)}')
            return redirect('mandados:visualizar', pk=pk)
    return render(request, 'mandados/excluir.html', {'mandado': mandado})

@login_required
def carrossel_fotos(request):
    # Buscar todas as fotos de mandados ativos, ordenadas por data de upload
    fotos = Foto.objects.filter(
        mandado__status='ativo'
    ).select_related('mandado').order_by('-data_upload')
    
    return render(request, 'mandados/carrossel.html', {'fotos': fotos})
