from django import forms
from .models import Mandado

class MandadoForm(forms.ModelForm):
    class Meta:
        model = Mandado
        fields = [
            'numero_processo',
            'nome_infrator',
            'data_nascimento',
            'cpf',
            'rg',
            'rji',
            'nome_social',
            'sexo',
            'cor',
            'mae',
            'pai',
            'endereco',
            'cidade',
            'estado',
            'crime',
            'data_expedicao',
            'data_validade',
            'regime_prisional',
            'pena_restante',
            'status'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_expedicao': forms.DateInput(attrs={'type': 'date'}),
            'data_validade': forms.DateInput(attrs={'type': 'date'}),
        } 