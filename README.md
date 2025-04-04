# Sistema de Gerenciamento de Mandados de Prisão

Sistema desenvolvido em Django para gerenciamento de mandados de prisão, com funcionalidades de importação automática de PDFs e reconhecimento facial.

## Funcionalidades

- Cadastro e gerenciamento de mandados de prisão
- Importação automática de dados de PDFs de mandados
- Reconhecimento facial para identificação de infratores
- Interface web responsiva e intuitiva
- Gerenciamento de fotos e documentos

## Requisitos

- Python 3.8+
- Django 5.2
- PyPDF2
- face_recognition
- Pillow
- Outras dependências listadas em requirements.txt

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
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

4. Configure o banco de dados:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Execute o servidor:
```bash
python manage.py runserver
```

## Estrutura do Projeto

- `mandados/` - Aplicação principal
  - `models.py` - Modelos de dados
  - `views.py` - Lógica de visualização
  - `urls.py` - Configuração de URLs
  - `utils.py` - Funções utilitárias
  - `templates/` - Templates HTML
  - `static/` - Arquivos estáticos

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 