from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.mandado import Mandado

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    mandados = Mandado.query.filter_by(status='ativo').order_by(Mandado.data_expedicao.desc()).limit(5).all()
    return render_template('main/index.html', mandados=mandados)

@bp.route('/dashboard')
@login_required
def dashboard():
    total_mandados = Mandado.query.count()
    mandados_ativos = Mandado.query.filter_by(status='ativo').count()
    mandados_cumpridos = Mandado.query.filter_by(status='cumprido').count()
    mandados_cancelados = Mandado.query.filter_by(status='cancelado').count()
    
    return render_template('main/dashboard.html',
                         total_mandados=total_mandados,
                         mandados_ativos=mandados_ativos,
                         mandados_cumpridos=mandados_cumpridos,
                         mandados_cancelados=mandados_cancelados) 