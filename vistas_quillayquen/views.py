from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Reserva
from django.views.decorators.csrf import csrf_exempt
import requests
from quillayquen1.telegram_secrets import TOKEN, CHAT_ID  # Importamos el token seguro

def inicio(request):
    return render(request, 'vistas_quillayquen/inicio.html')

def procesar_reserva(request):
    """
    Vista para procesar el formulario de reserva.
    Ahora con notificación a Telegram
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

            # Enviar notificación a Telegram
            mensaje_telegram = f"""
📅 *Nueva Reserva Confirmada* 🎉
👤 *Nombre:* {nombre}
📅 *Fecha:* {fecha}
⏰ *Hora:* {hora}
            """.strip()
            
            requests.post(
                f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                json={
                    'chat_id': CHAT_ID,
                    'text': mensaje_telegram,
                    'parse_mode': 'Markdown'
                }
            )

            messages.success(request, f"Reserva realizada con éxito para {nombre} el {fecha} a las {hora}.")
            return render(request, 'reserva_exitosa.html', {
                'nombre': nombre,
                'fecha': fecha,
                'hora': hora
            })

        except Exception as e:
            messages.error(request, f"Hubo un problema al procesar tu reserva: {str(e)}")
            return redirect('inicio')
    
    return redirect('inicio')

@csrf_exempt
def enviar_cotizacion(request):
    """
    Nueva vista para manejar el formulario de cotización
    """
    if request.method == 'POST':
        try:
            data = request.POST
            mensaje = f"""
📋 *Nueva Solicitud de Cotización* 📝
👤 *Nombre:* {data.get('nombre', '')}
📞 *Teléfono:* {data.get('telefono', '')}
🏠 *Recinto:* {data.get('tipoRecinto', '')}
🎉 *Evento:* {data.get('tipoEvento', '')}
📅 *Fecha:* {data.get('fechaEvento', '')}
📝 *Detalles:* {data.get('descripcion', 'Ninguno')}
            """.strip()

            response = requests.post(
                f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                json={
                    'chat_id': CHAT_ID,
                    'text': mensaje,
                    'parse_mode': 'Markdown'
                }
            )
            
            return JsonResponse({'status': 'success' if response.ok else 'error'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def listar_reservas(request):
    """Vista para listar todas las reservas"""
    try:
        reservas = Reserva.objects.all()
        return render(request, 'lista_reservas.html', {'reservas': reservas})
    except Exception as e:
        messages.error(request, f"Hubo un problema al obtener las reservas: {str(e)}")
        return HttpResponse("Error al obtener el listado de reservas.")