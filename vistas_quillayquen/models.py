from django.db import models
from django.utils import timezone  # Asegúrate de importar timezone

class Reserva(models.Model):
    # Campos del modelo
    nombre = models.CharField(max_length=100)
    fecha_reserva = models.DateTimeField(default=timezone.now)  # Valor por defecto
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
from django.db import models

class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    telefono = models.CharField(max_length=20)  # Nuevo campo teléfono
    recinto = models.CharField(max_length=20, choices=[('Recinto 1', 'Recinto 1'), ('Recinto 2', 'Recinto 2')], default='Recinto 1')
    cancha = models.CharField(max_length=20, choices=[('Cancha 1', 'Cancha 1'), ('Cancha 2', 'Cancha 2')], default='Cancha 1')

    def __str__(self):
        return f"Reserva de {self.nombre} para el {self.fecha} a las {self.hora} en {self.recinto} - {self.cancha}"

