import os
import subprocess
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mandados_db.settings')
django.setup()

def run_migrations():
    """Executa as migrações do banco de dados."""
    print("Executando migrações do banco de dados...")
    subprocess.run(['python', 'manage.py', 'migrate'])

def create_superuser():
    """Cria o superusuário administrativo se não existir."""
    from django.contrib.auth.models import User
    
    if not User.objects.filter(username='admin').exists():
        print("Criando superusuário administrativo...")
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("Superusuário criado com sucesso!")
    else:
        print("Superusuário já existe.")

def collect_static():
    """Coleta arquivos estáticos."""
    print("Coletando arquivos estáticos...")
    subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'])

def run_server():
    """Inicia o servidor Django."""
    print("Iniciando servidor Django...")
    subprocess.run(['python', 'manage.py', 'runserver'])

if __name__ == '__main__':
    run_migrations()
    create_superuser()
    collect_static()
    run_server() 