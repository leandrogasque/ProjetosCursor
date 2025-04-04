import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mandados_db.settings')
django.setup()

from django.contrib.auth.models import User
from django.db.utils import IntegrityError

def create_superuser():
    """Cria um superusuário se ele não existir."""
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print('Superusuário criado com sucesso!')
        else:
            print('O superusuário já existe.')
    except IntegrityError:
        print('Erro ao criar superusuário. Ele pode já existir.')
    except Exception as e:
        print(f'Erro inesperado: {str(e)}')

if __name__ == '__main__':
    create_superuser() 