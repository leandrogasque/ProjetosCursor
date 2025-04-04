from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        # Importar modelos primeiro
        from app.models.user import User
        from app.models.mandado import Mandado

        # Criar todas as tabelas
        db.create_all()  # Cria todas as tabelas se não existirem

        # Registrar blueprints
        from app.routes import auth, main, mandados
        app.register_blueprint(auth.bp)
        app.register_blueprint(main.bp)
        app.register_blueprint(mandados.bp)

        # Criar usuário admin se não existir
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin',
                last_login=datetime.utcnow()
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    return app 