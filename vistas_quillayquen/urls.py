from django.urls import path
from . import views
from vistas_quillayquen.views import enviar_telegram  # Importa la vista de Telegram

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Ruta principal
    path('procesar-reserva/', views.procesar_reserva, name='procesar_reserva'),
    path('listar-reservas/', views.listar_reservas, name='listar_reservas'),
    path('enviar-telegram/', enviar_telegram, name='enviar_telegram'),  # Nueva ruta
]
