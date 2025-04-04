# Sistema de Gerenciamento de Mandados de Prisão

Sistema desenvolvido em Django para gerenciamento de mandados de prisão, com funcionalidades de importação automática de PDFs e reconhecimento facial.

## Funcionalidades

- Cadastro e gerenciamento de mandados de prisão
- Importação automática de dados de PDFs de mandados
- Reconhecimento facial para identificação de infratores
- Interface web responsiva e intuitiva
- Gerenciamento de fotos e documentos
- Dashboard com estatísticas e gráficos
- Autenticação e controle de acesso

## Melhorias Implementadas

### Migração para Django
- Migração completa de Flask para Django 5.2
- Remocão de código duplicado e redundante
- Centralização da lógica em um único framework

### Segurança
- Configuração da SECRET_KEY via variáveis de ambiente (.env)
- Modo DEBUG configurável por ambiente
- Proteção CSRF em todos os formulários
- Rotas protegidas por autenticação
- Configurações de produção documentadas

### Interface
- Design responsivo com Bootstrap 5
- Utilização do Crispy Forms para melhor exibição de formulários
- Dashboard interativo com gráficos usando Chart.js
- Navegação intuitiva e moderna

### Estrutura
- Organização clara de pastas e arquivos
- Separação de templates, modelos e views
- Configurações centralizadas
- Scripts de automação para facilitar a instalação

## Requisitos

- Python 3.8+
- Django 5.2
- PyPDF2 3.0.1
- Pillow 11.1.0+
- python-dateutil 2.8.2
- Outras dependências listadas em requirements.txt

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/leandrogasque/ProjetosCursor.git
cd ProjetosCursor
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o arquivo .env na raiz do projeto com suas variáveis de ambiente:
```
SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Execute as migrações e inicie o servidor:
```bash
python runserver.py
```

Este script irá:
- Executar as migrações do banco de dados
- Criar um superusuário admin (se não existir)
- Coletar os arquivos estáticos
- Iniciar o servidor Django

## Acessando o Sistema

- Acesse o sistema através de http://localhost:8000
- Para acessar o painel administrativo, vá para http://localhost:8000/admin
- Use as credenciais padrão para administrador:
  - Usuário: admin
  - Senha: admin123

**Importante:** Altere a senha padrão do administrador após o primeiro login!

## Estrutura do Projeto

- `mandados/` - Aplicação principal
  - `models.py` - Modelos de dados
  - `views.py` - Lógica de visualização
  - `urls.py` - Configuração de URLs
  - `utils.py` - Funções utilitárias
  - `templates/` - Templates HTML
  - `static/` - Arquivos estáticos

- `mandados_db/` - Configurações do projeto Django
  - `settings.py` - Configurações do Django
  - `urls.py` - URLs principais

- `media/` - Arquivos enviados pelos usuários
  - `uploads/` - Fotos e documentos de mandados

- `static/` - Arquivos estáticos do projeto

- `staticfiles/` - Arquivos estáticos coletados para produção

## Scripts Utilitários

- `runserver.py` - Script para iniciar o servidor com todas as configurações
- `create_superuser.py` - Script para criar o superusuário administrativo

## Configurações de Segurança

Para configurar o projeto para ambiente de produção:

1. Altere as seguintes configurações no arquivo .env:
```
SECRET_KEY=uma-chave-secreta-longa-e-complexa
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
```

2. Configure um servidor web como Nginx ou Apache como proxy reverso.

3. Use um servidor WSGI como Gunicorn para executar a aplicação.

## Problemas Corrigidos

- Mistura de frameworks (Flask e Django) causando conflitos
- Chaves de segurança expostas no código
- Duplicação de lógica de autenticação
- Problemas de inconsistência de templates
- Configurações de banco de dados duplicadas
- Configurações inadequadas para produção

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 