import re
from datetime import datetime
from dateutil import parser
from PyPDF2 import PdfReader

def find_date_near_keywords(text, keywords, max_distance=100):
    """
    Procura por uma data próxima a palavras-chave no texto.
    Retorna a primeira data encontrada dentro da distância máxima.
    """
    # Padrão para encontrar datas no formato DD/MM/YYYY
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    
    # Encontra todas as datas no texto
    dates = [(m.start(), m.group()) for m in re.finditer(date_pattern, text)]
    
    # Para cada palavra-chave
    for keyword in keywords:
        # Encontra a posição da palavra-chave
        keyword_pos = text.find(keyword)
        if keyword_pos == -1:
            continue
            
        # Procura por datas próximas
        for date_pos, date_str in dates:
            # Calcula a distância entre a data e a palavra-chave
            distance = abs(date_pos - keyword_pos)
            if distance <= max_distance:
                return date_str
    
    return None

def extract_mandado_data(pdf_file):
    """
    Extrai dados de um arquivo PDF de mandado de prisão.
    Retorna um dicionário com os dados extraídos.
    """
    try:
        # Lê o PDF
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Padrões de busca com múltiplas variações
        patterns = {
            'numero_processo': [
                r'N[º°] do processo:?\s*([\d\.-]+)',
                r'Processo n[º°]\s*([\d\.-]+)',
                r'N[º°] do Mandado:?\s*([\d\.-]+)',
            ],
            'nome_infrator': [
                r'Nome da Pessoa:?\s*([^\n]+?)(?=\s*CPF:)',
                r'Nome do Infrator:?\s*([^\n]+)',
                r'Nome do R[ée]u:?\s*([^\n]+)',
            ],
            'data_nascimento': [
                r'Data de Nascimento:?\s*(\d{2}/\d{2}/\d{4})',
                r'Nascimento:?\s*(\d{2}/\d{2}/\d{4})',
            ],
            'cpf': [
                r'CPF:?\s*(\d{3}\.\d{3}\.\d{3}-\d{2})',
                r'CPF:?\s*(\d{11})',
            ],
            'rg': [
                r'RG:?\s*(\d+[^\n]*)',
            ],
            'rji': [
                r'RJI:?\s*([^\n]+)',
            ],
            'nome_social': [
                r'Nome Social:?\s*([^\n]+)',
            ],
            'sexo': [
                r'Sexo:?\s*([^\n]+)',
            ],
            'cor': [
                r'Cor:?\s*([^\n]+)',
            ],
            'mae': [
                r'(?:Filiação|mãe):?\s*([^(\n]+?)\s*(?:\(mãe\)|e)',
            ],
            'pai': [
                r'(?:pai\)|e)\s*([^(\n]+?)(?:\(pai\)|$|\n)',
            ],
            'endereco': [
                r'Endereços?\s*([^\n]+)',
                r'Residência:?\s*([^\n]+)',
            ],
            'cidade': [
                r'([^,]+)\s*-\s*SP',
                r'Cidade:?\s*([^\n]+)',
            ],
            'estado': [
                r'-\s*([A-Z]{2})',
                r'Estado:?\s*([A-Z]{2})',
            ],
            'crime': [
                r'Tipificação Penal:?\s*Lei:?\s*([^\n]+)',
                r'Crime:?\s*([^\n]+)',
                r'Fato:?\s*([^\n]+)',
            ],
            'data_validade': [
                r'Data de validade:?\s*(\d{2}/\d{2}/\d{4})',
                r'Validade:?\s*(\d{2}/\d{2}/\d{4})',
            ],
            'regime_prisional': [
                r'Regime Prisional:?\s*([^\n]+)',
            ],
            'pena_restante': [
                r'Pena restante:?\s*([^\n]+)',
            ],
        }

        # Campos obrigatórios
        required_fields = ['numero_processo', 'nome_infrator', 'data_nascimento', 'cpf', 'crime']
        missing_fields = []

        # Extrai os dados
        data = {}
        for field, pattern_list in patterns.items():
            value = None
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    # Converte datas para o formato do Django
                    if field in ['data_nascimento', 'data_expedicao', 'data_validade']:
                        try:
                            date = parser.parse(value, dayfirst=True)
                            value = date.strftime('%Y-%m-%d')
                        except:
                            value = None
                    break
            data[field] = value
            if field in required_fields and value is None:
                missing_fields.append(field)

        # Trata campos especiais
        if data.get('nome_social') == 'Não Informado':
            data['nome_social'] = None

        # Tenta encontrar a data de expedição usando palavras-chave
        data_expedicao = None
        keywords = [
            'EXPEDIÇÃO', 'EMITIDO', 'MANDADO', 'EMISSÃO',
            'DATA DO MANDADO', 'DATA DE EXPEDIÇÃO', 'DATA DE EMISSÃO',
            'EXPEDIDO', 'EMITIDO EM', 'DATA DE EXPEDIÇÃO DO MANDADO',
            'DATA DE EXPEDIÇÃO DO MANDADO DE PRISÃO', 'MANDADO DE PRISÃO',
            'EXPEDIÇÃO DO MANDADO', 'EMISSÃO DO MANDADO'
        ]
        date_str = find_date_near_keywords(text, keywords)
        if date_str:
            try:
                date = parser.parse(date_str, dayfirst=True)
                data_expedicao = date.strftime('%Y-%m-%d')
            except:
                pass

        # Se ainda não encontrou a data de expedição, tenta usar a data atual
        if data_expedicao is None:
            data_expedicao = datetime.now().strftime('%Y-%m-%d')
        
        # Adiciona a data de expedição aos dados
        data['data_expedicao'] = data_expedicao

        # Verifica campos obrigatórios
        if missing_fields:
            fields_str = ', '.join(missing_fields)
            raise Exception(f'Campos obrigatórios não encontrados no PDF: {fields_str}')

        # Define o status como ativo por padrão
        data['status'] = 'ativo'

        return data

    except Exception as e:
        raise Exception(f"Erro ao processar o PDF: {str(e)}") 