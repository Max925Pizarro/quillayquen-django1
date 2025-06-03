from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Reserva

from django.views.decorators.csrf import csrf_exempt
import json

def inicio(request):
    return render(request, 'vistas_quillayquen/inicio.html')  # Ruta completa

def procesar_reserva(request):
    """
    Vista para procesar el formulario de reserva.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        # Validación básica
        if not nombre or not fecha or not hora:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('inicio')

        try:
            # Guardar la reserva en la base de datos
            reserva = Reserva(nombre=nombre, fecha=fecha, hora=hora)
            reserva.save()

            # Mensaje de éxito
            messages.success(request, f"Reserva realizada con éxito para {nombre} el {fecha} a las {hora}.")
            
            return render(request, 'reserva_exitosa.html', {
                'nombre': nombre,
                'fecha': fecha,
                'hora': hora
            })

        except Exception as e:
            # Si hay un error guardando la reserva
            messages.error(request, f"Hubo un problema al procesar tu reserva: {str(e)}")
            return redirect('inicio')
    
    # Si no es POST, redirigir a la página de inicio
    return redirect('inicio')

def listar_reservas(request):
    """Vista para listar todas las reservas"""
    try:
        reservas = Reserva.objects.all()
        return render(request, 'lista_reservas.html', {'reservas': reservas})

    except Exception as e:
        messages.error(request, f"Hubo un problema al obtener las reservas: {str(e)}")
        return HttpResponse("Error al obtener el listado de reservas.")

@csrf_exempt
def cancelar_reserva(request):
    """
    Vista para cancelar una reserva mediante POST con JSON.
    Se espera recibir 'rut' y opcionalmente otros datos para identificar la reserva.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rut = data.get('rut', '').strip()
            fecha = data.get('fecha', '').strip()
            hora = data.get('hora', '').strip()

            if not rut:
                return JsonResponse({'success': False, 'message': 'El RUT es obligatorio.'})

            # Buscar la reserva que coincida con los datos proporcionados
            reservas = Reserva.objects.filter(rut=rut)
            if fecha:
                reservas = reservas.filter(fecha=fecha)
            if hora:
                reservas = reservas.filter(hora=hora)

            if not reservas.exists():
                return JsonResponse({'success': False, 'message': 'No se encontró ninguna reserva con los datos proporcionados.'})

            # Eliminar la reserva (o reservas) encontradas
            count, _ = reservas.delete()

            return JsonResponse({'success': True, 'message': f'Se cancelaron {count} reserva(s) correctamente.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'JSON inválido.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al cancelar la reserva: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})
