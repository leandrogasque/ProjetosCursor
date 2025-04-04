from django.contrib import admin
from .models import Mandado, Foto

class FotoInline(admin.TabularInline):
    model = Foto
    extra = 1

@admin.register(Mandado)
class MandadoAdmin(admin.ModelAdmin):
    list_display = ('numero_processo', 'nome_infrator', 'crime', 'data_expedicao', 'status')
    list_filter = ('status', 'data_expedicao')
    search_fields = ('numero_processo', 'nome_infrator', 'crime')
    date_hierarchy = 'data_expedicao'
    inlines = [FotoInline]

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('mandado', 'descricao', 'data_upload')
    list_filter = ('data_upload',)
    search_fields = ('descricao', 'mandado__numero_processo')
    date_hierarchy = 'data_upload'
