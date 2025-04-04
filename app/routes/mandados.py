import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.mandado import Mandado, Foto
from datetime import datetime

bp = Blueprint('mandados', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Garantir que o diretório de uploads existe
def ensure_upload_folder():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    print(f"Verificando diretório de uploads: {upload_folder}")
    print(f"Diretório existe? {os.path.exists(upload_folder)}")
    
    if not os.path.exists(upload_folder):
        try:
            os.makedirs(upload_folder, exist_ok=True)
            print(f"Diretório de uploads criado: {upload_folder}")
        except Exception as e:
            print(f"Erro ao criar diretório de uploads: {str(e)}")
            raise
    
    # Verificar permissões do diretório
    try:
        test_file = os.path.join(upload_folder, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print(f"Permissões de escrita no diretório de uploads: OK")
    except Exception as e:
        print(f"Erro ao verificar permissões do diretório de uploads: {str(e)}")
        raise
    
    return upload_folder

@bp.route('/mandados')
@login_required
def listar_mandados():
    page = request.args.get('page', 1, type=int)
    mandados = Mandado.query.order_by(Mandado.data_expedicao.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('mandados/listar.html', mandados=mandados)

@bp.route('/mandados/novo', methods=['GET', 'POST'])
@login_required
def novo_mandado():
    if request.method == 'POST':
        try:
            # Verificar se o número do processo já existe
            numero_processo = request.form['numero_processo']
            if Mandado.query.filter_by(numero_processo=numero_processo).first():
                flash('Já existe um mandado cadastrado com este número de processo.', 'error')
                return redirect(url_for('mandados.novo_mandado'))

            upload_folder = ensure_upload_folder()  # Garantir que o diretório de uploads existe
            print(f"Diretório de uploads para novo mandado: {upload_folder}")
            
            mandado = Mandado(
                numero_processo=numero_processo,
                nome_infrator=request.form['nome_infrator'],
                data_nascimento=datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d'),
                cpf=request.form['cpf'],
                rg=request.form['rg'],
                endereco=request.form['endereco'],
                cidade=request.form['cidade'],
                estado=request.form['estado'],
                crime=request.form['crime'],
                data_expedicao=datetime.strptime(request.form['data_expedicao'], '%Y-%m-%d'),
                data_validade=datetime.strptime(request.form['data_validade'], '%Y-%m-%d') if request.form['data_validade'] else None,
                observacoes=request.form['observacoes'],
                status=request.form['status'],
                registrado_por_id=current_user.id
            )
            
            db.session.add(mandado)
            db.session.commit()
            print(f"Mandado criado com ID: {mandado.id}")
            
            # Upload de fotos
            if 'fotos' in request.files:
                files = request.files.getlist('fotos')
                print(f"Número de arquivos recebidos: {len(files)}")
                
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(upload_folder, filename)
                        print(f"Salvando arquivo: {filepath}")
                        print(f"Tipo de arquivo: {type(file)}")
                        print(f"Nome do arquivo: {file.filename}")
                        print(f"Tamanho do arquivo: {file.content_length if hasattr(file, 'content_length') else 'N/A'}")
                        
                        try:
                            file.save(filepath)
                            print(f"Arquivo salvo com sucesso: {filepath}")
                            print(f"Arquivo existe após salvar? {os.path.exists(filepath)}")
                            print(f"Tamanho do arquivo salvo: {os.path.getsize(filepath)} bytes")
                            
                            foto = Foto(
                                mandado_id=mandado.id,
                                filename=filename,
                                descricao=request.form.get('descricao_foto', '')
                            )
                            db.session.add(foto)
                            print(f"Foto adicionada ao banco de dados: {filename}")
                        except Exception as e:
                            print(f"Erro ao salvar arquivo {filename}: {str(e)}")
                            flash(f'Erro ao salvar a foto {filename}: {str(e)}', 'error')
                    else:
                        print(f"Arquivo não permitido ou vazio: {file.filename if file else 'None'}")
                
                try:
                    db.session.commit()
                    print("Fotos salvas no banco de dados com sucesso")
                except Exception as e:
                    print(f"Erro ao salvar fotos no banco de dados: {str(e)}")
                    db.session.rollback()
                    flash('Erro ao salvar as fotos no banco de dados.', 'error')
            else:
                print("Nenhum arquivo de foto recebido")
            
            flash('Mandado de prisão cadastrado com sucesso!')
            return redirect(url_for('mandados.listar_mandados'))
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao cadastrar mandado: {str(e)}")
            flash(f'Erro ao cadastrar mandado: {str(e)}', 'error')
            return redirect(url_for('mandados.novo_mandado'))
    
    return render_template('mandados/novo.html')

@bp.route('/mandados/<int:id>')
@login_required
def visualizar_mandado(id):
    mandado = Mandado.query.get_or_404(id)
    print(f"Visualizando mandado ID: {id}")
    print(f"Número de fotos: {len(mandado.fotos)}")
    for foto in mandado.fotos:
        print(f"Foto: {foto.filename}, Caminho: {os.path.join(current_app.config['UPLOAD_FOLDER'], foto.filename)}")
        print(f"Arquivo existe? {os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], foto.filename))}")
    return render_template('mandados/visualizar.html', mandado=mandado)

@bp.route('/mandados/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_mandado(id):
    mandado = Mandado.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            mandado.numero_processo = request.form['numero_processo']
            mandado.nome_infrator = request.form['nome_infrator']
            mandado.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d')
            mandado.cpf = request.form['cpf']
            mandado.rg = request.form['rg']
            mandado.endereco = request.form['endereco']
            mandado.cidade = request.form['cidade']
            mandado.estado = request.form['estado']
            mandado.crime = request.form['crime']
            mandado.data_expedicao = datetime.strptime(request.form['data_expedicao'], '%Y-%m-%d')
            mandado.data_validade = datetime.strptime(request.form['data_validade'], '%Y-%m-%d') if request.form['data_validade'] else None
            mandado.observacoes = request.form['observacoes']
            mandado.status = request.form['status']
            
            db.session.commit()
            print(f"Mandado atualizado com ID: {mandado.id}")
            
            # Upload de novas fotos
            if 'fotos' in request.files:
                upload_folder = ensure_upload_folder()
                print(f"Diretório de uploads para edição: {upload_folder}")
                files = request.files.getlist('fotos')
                print(f"Número de arquivos recebidos na edição: {len(files)}")
                
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(upload_folder, filename)
                        print(f"Salvando arquivo na edição: {filepath}")
                        print(f"Tipo de arquivo: {type(file)}")
                        print(f"Nome do arquivo: {file.filename}")
                        print(f"Tamanho do arquivo: {file.content_length if hasattr(file, 'content_length') else 'N/A'}")
                        
                        try:
                            file.save(filepath)
                            print(f"Arquivo salvo com sucesso na edição: {filepath}")
                            print(f"Arquivo existe após salvar? {os.path.exists(filepath)}")
                            print(f"Tamanho do arquivo salvo: {os.path.getsize(filepath)} bytes")
                            
                            foto = Foto(
                                mandado_id=mandado.id,
                                filename=filename,
                                descricao=request.form.get('descricao_foto', '')
                            )
                            db.session.add(foto)
                            print(f"Foto adicionada ao banco de dados na edição: {filename}")
                        except Exception as e:
                            print(f"Erro ao salvar arquivo {filename} na edição: {str(e)}")
                            flash(f'Erro ao salvar a foto {filename}: {str(e)}', 'error')
                    else:
                        print(f"Arquivo não permitido ou vazio na edição: {file.filename if file else 'None'}")
                
                try:
                    db.session.commit()
                    print("Fotos salvas no banco de dados com sucesso na edição")
                except Exception as e:
                    print(f"Erro ao salvar fotos no banco de dados na edição: {str(e)}")
                    db.session.rollback()
                    flash('Erro ao salvar as fotos no banco de dados.', 'error')
            else:
                print("Nenhum arquivo de foto recebido na edição")
            
            flash('Mandado de prisão atualizado com sucesso!')
            return redirect(url_for('mandados.visualizar_mandado', id=mandado.id))
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar mandado: {str(e)}")
            flash(f'Erro ao atualizar mandado: {str(e)}', 'error')
            return redirect(url_for('mandados.editar_mandado', id=mandado.id))
    
    return render_template('mandados/editar.html', mandado=mandado)

@bp.route('/mandados/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_mandado(id):
    if not current_user.is_admin():
        flash('Apenas administradores podem excluir mandados.')
        return redirect(url_for('mandados.listar_mandados'))
    
    mandado = Mandado.query.get_or_404(id)
    
    # Excluir fotos do sistema de arquivos
    for foto in mandado.fotos:
        try:
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], foto.filename)
            print(f"Excluindo arquivo: {filepath}")
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Arquivo excluído com sucesso: {filepath}")
            else:
                print(f"Arquivo não encontrado para exclusão: {filepath}")
        except Exception as e:
            print(f"Erro ao excluir arquivo {foto.filename}: {str(e)}")
    
    db.session.delete(mandado)
    db.session.commit()
    
    flash('Mandado de prisão excluído com sucesso!')
    return redirect(url_for('mandados.listar_mandados')) 