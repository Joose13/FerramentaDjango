import json
import requests
import urllib3
from django.http import HttpResponse
from io import BytesIO

urllib3.disable_warnings()

def get_data(base_url):
    try:
        response = requests.get(base_url, timeout=10, verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")
        return None

def save_data(use_BK, use_MC):
    all_data = {"BK": {}, "MC": {}}

    BK_base_url = "http://192.168.1.3:3000/api/tiendas"
    MC_base_url = "http://192.168.1.3:4000/api/tiendas"

    if use_BK:
        BK_tenant = "BK"
        BK_data = get_data(BK_base_url)
        if BK_data:
            all_data["BK"] = BK_data

    if use_MC:
        MC_tenant = "MC"
        MC_data = get_data(MC_base_url)
        if MC_data:
            all_data["MC"] = MC_data

    # Convertir a JSON y escribir en BytesIO para manejarlo como archivo
    json_data = json.dumps(all_data, ensure_ascii=False, indent=4)
    json_bytes = BytesIO(json_data.encode("utf-8"))

    # Crear la respuesta con el archivo adjunto
    response = HttpResponse(json_bytes.getvalue(), content_type="application/json")
    response["Content-Disposition"] = 'attachment; filename="copia_tiendas.json"'
    response["Content-Length"] = str(len(json_bytes.getvalue()))  # Tamaño correcto

    return response

