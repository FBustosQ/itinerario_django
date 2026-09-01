from django.shortcuts import render, redirect
import os
import json
from datetime import datetime, timedelta 

ARCHIVO_JSON = os.path.join(
    os.path.dirname(__file__), 'data', 'itinerarios.json'
)

def cargar_itinerarios():
    with open(ARCHIVO_JSON, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def guardar_itinerario(itinerarios):
    with open(ARCHIVO_JSON, 'w', encoding='utf-8') as archivo:
        json.dump(
            itinerarios,
            archivo,
            ensure_ascii=False,
            indent=4
        )

def inicio(request):
    itinerarios = cargar_itinerarios()
    return render(request, 'index.html', {'itinerarios': itinerarios})

def crear(request):
    if request.method == 'POST':
        itinerarios = cargar_itinerarios()

        nuevo_id = max(
            [
                itinerario['id'] for itinerario in itinerarios
            ],
            default=0
        ) + 1
        destino = request.POST.get('destino', '')
        letra_d = destino[0].upper() if destino else 'X'
        origen = request.POST.get('origen', '')
        letra_o = origen[0].upper() if origen else 'X'

        conteo_origen = len([
            itinerario for itinerario in itinerarios 
            if itinerario['origen'] == origen
            ])

        numero_itinerario = f"{letra_o}{letra_d}{conteo_origen + 1}"

        hora_salida_raw = request.POST.get('salida')
        hora_salida_obj = datetime.strptime(hora_salida_raw, '%H:%M')
        hora_salida = hora_salida_obj.strftime('%H:%M')

        duracion_minutos = int(request.POST.get('duracion', 0))
        hora_llegada = (hora_salida_obj + timedelta(minutes=duracion_minutos)).strftime('%H:%M')

        nuevo_itinerario = {
            "id": nuevo_id,
            "numero": numero_itinerario,
            "origen": request.POST.get('origen'),
            "destino": request.POST.get('destino'),
            "salida": hora_salida,
            "llegada": hora_llegada,
            "frecuencia": int(request.POST.get('frecuencia')),
            "estado": request.POST.get('estado')
        }
        itinerarios.append(nuevo_itinerario)

        guardar_itinerario(itinerarios)

        return redirect('inicio')
    
    # Para GET - mostrar el formulario
    return render(request, 'crear.html')

def detalle(request, id):
    itinerarios = cargar_itinerarios()
    itinerario_encontrado = None
    horarios = []

    # Buscar el itinerario por ID
    for itinerario in itinerarios:
        if itinerario['id'] == id:
            itinerario_encontrado = itinerario
            break

    # Solo generar horarios si se encontró el itinerario
    if itinerario_encontrado:
        hora_salida = datetime.strptime(str(itinerario_encontrado['salida']), '%H:%M')
        hora_llegada = datetime.strptime(str(itinerario_encontrado['llegada']), '%H:%M')
        duracion = hora_llegada - hora_salida
        frecuencia_minutos = itinerario_encontrado['frecuencia']
        
        for i in range(5):
            frecuencia = frecuencia_minutos * i
            salidas = hora_salida + timedelta(minutes=frecuencia)
            llegadas = salidas + duracion
            horarios.append({
                'salida': salidas.strftime('%H:%M'),
                'llegada': llegadas.strftime('%H:%M'),
            })
    
    
    context = {
        'itinerario': itinerario_encontrado,
        'horarios': horarios,
    }
    
    
    return render(request, 'detalle.html', context)

