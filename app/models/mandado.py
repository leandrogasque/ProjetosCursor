from app import db
from datetime import datetime

class Mandado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_processo = db.Column(db.String(50), unique=True, nullable=False)
    nome_infrator = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date)
    cpf = db.Column(db.String(14))
    rg = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    crime = db.Column(db.String(200), nullable=False)
    data_expedicao = db.Column(db.Date, nullable=False)
    data_validade = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default='ativo')  # ativo, cumprido, cancelado
    observacoes = db.Column(db.Text)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    registrado_por_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fotos = db.relationship('Foto', backref='mandado', lazy=True, cascade='all, delete-orphan')

class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(200))
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)
    mandado_id = db.Column(db.Integer, db.ForeignKey('mandado.id'), nullable=False) 