from django.urls import path
from . import views

app_name = 'mandados'

urlpatterns = [
    path('', views.listar_mandados, name='listar'),
    path('novo/', views.novo_mandado, name='novo'),
    path('<int:pk>/', views.visualizar_mandado, name='visualizar'),
    path('<int:pk>/editar/', views.editar_mandado, name='editar'),
    path('<int:pk>/excluir/', views.excluir_mandado, name='excluir'),
    path('reconhecimento/', views.carrossel_fotos, name='carrossel'),
] 