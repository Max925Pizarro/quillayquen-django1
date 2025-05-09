from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Ruta principal
    path('procesar-reserva/', views.procesar_reserva, name='procesar_reserva'),
    path('listar-reservas/', views.listar_reservas, name='listar_reservas'),
]
