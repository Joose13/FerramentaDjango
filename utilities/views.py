from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from io import BytesIO
from . import copia_gds
from . import copia_tiendas
from . import pedidos_legacy
from . import pedidos_mongo
from . import maxprep
from . import weekendays
import mysql.connector
import json

# Vista para la página principal
def index(request):
    return render(request, 'index.html')

# Vista para la selección del módulo a ejecutar
def seleccionar_modulo(request):
    if request.method == "POST":
        # Verificamos qué módulo se ha seleccionado
        modulo_seleccionado = request.POST.get('modulo')
        
        # Redirigimos a la página de configuración del módulo seleccionado
        if modulo_seleccionado == "copia_gds":
            return render(request, 'copiar_grupos.html', {'modulo': modulo_seleccionado})
        elif modulo_seleccionado == "copia_tiendas":
            return render(request, 'copiar_tiendas.html', {'modulo': modulo_seleccionado})
        elif modulo_seleccionado == "maxprep":
            return render(request, 'maxprep.html', {'modulo': modulo_seleccionado})
        elif modulo_seleccionado == "weekendays":
            return render(request, 'weekend_days.html', {'modulo': modulo_seleccionado})
    
    return redirect('index')  # Si no se recibe un formulario POST, redirigimos a la página principal.

# Vista para ejecutar el módulo con las opciones seleccionadas
def ejecutar_copia(request):
    if request.method == "POST":
        # Recuperamos las opciones seleccionadas por el usuario

        use_BK = 'BK' in request.POST  # Si 'BK' está en request.POST, el checkbox fue marcado
        use_MC = 'MC' in request.POST  # Lo mismo para 'MC'
        
        # Ejecutamos la función del módulo copiar_gds
        resultado = copia_gds.save_data(use_BK, use_MC)
        
        # Mostramos el resultado en una página de éxito
        return resultado
    
    return redirect('index')  # Si no se recibe un formulario POST, redirigimos a la página principal.

def ejecutar_copia_tiendas(request):
    if request.method == "POST":
        # Recuperamos las opciones seleccionadas por el usuario
        use_BK = 'BK' in request.POST
        use_MC = 'MC' in request.POST
        
        # Ejecutamos la función del módulo copiar_gds
        resultado = copia_tiendas.save_data(use_BK, use_MC)
        
        # Mostramos el resultado en una página de éxito
        return resultado
    
    return redirect('index')  # Si no se recibe un formulario POST, redirigimos a la página principal.

# Nueva vista para obtener el total de pedidos de las localizaciones
def contar_pedidos_total_view(request):
    total_legacy = None
    total_iop = None

    if request.method == "POST":
        store_ids = request.POST.get("store_ids")
        conexion = request.POST.get("conexion")

        try:
            total_legacy = pedidos_legacy.contar_pedidos(store_ids, conexion)
        except Exception as e:
            total_legacy = f"Error Legacy: {str(e)}"

        try:
            total_iop = pedidos_mongo.contar_pedidos_iop(store_ids, conexion)
        except Exception as e:
            total_iop = f"Error Mongo: {str(e)}"

    return render(request, "index.html", {
        "total_legacy": total_legacy,
        "total_iop": total_iop,
    })

#Vista para ejecutar el módulo de fechas de preparación
def insertar_maxprep(request):
    if request.method == "POST":
        try:
            gd_list = request.POST.get('gd_list', '').split(',')
            utc_offset = float(request.POST.get('utc_offset', 0))
            opcion = int(request.POST.get('opcion', -1))
            fechas = json.loads(request.POST.get('fechas', '[]'))

            results = maxprep.generar_json(gd_list, utc_offset, opcion, fechas)

            if results:
                response = HttpResponse(
                    json.dumps(results, indent=4, ensure_ascii=False),
                    content_type='application/json'
                )
                response['Content-Disposition'] = 'attachment; filename="resultados_maxprep.json"'
                return response
            else:
                return JsonResponse({"message": "No se encontraron datos válidos."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return redirect('index')  # Si no se recibe un formulario POST, redirigimos a la página principal.

def weekend_days_view(request):
    if request.method == "POST":
        cadena = request.POST.get("cadena", "").strip()
        tipo = request.POST.get("tipo", "").strip()
        mercados_raw = request.POST.get("mercados", "")
        mercados = [m.strip().upper() for m in mercados_raw.split(",") if m.strip()]

        try:
            json_data = weekendays.generar_datos_weekend(cadena, mercados, tipo)
            buffer = BytesIO(json_data.encode("utf-8"))

            filename = f"weekend_days_{cadena}.json"
            response = HttpResponse(buffer.getvalue(), content_type="application/json")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            response["Content-Length"] = str(len(buffer.getvalue()))
            return response

        except Exception as e:
            return render(request, "weekend_days.html", {
                "error": str(e)
            })
    
    return redirect('index')  # Si no se recibe un formulario POST, redirigimos a la página principal.
