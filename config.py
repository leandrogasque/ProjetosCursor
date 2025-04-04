import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Configurações que podem ser utilizadas pelo Django
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media/uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size 