import json
import requests
import urllib3

urllib3.disable_warnings()

TIPOS = {
    "Viernes, Sábado": ["FRIDAY", "SATURDAY"],
    "Domingo": ["SUNDAY"],
    "Sin definir": [],
    "Fin de semana": ["SATURDAY", "SUNDAY"]
}

CADENA_URLS = {
    "BK": "http://192.168.1.3:3000/api/grupos",
    "MC": "http://192.168.1.3:4000/api/grupos"
}

def obtener_datos_desde_api(cadena):
    url = CADENA_URLS.get(cadena)
    if not url:
        raise ValueError("Cadena no válida")

    response = requests.get(url, verify=False, timeout=10)
    response.raise_for_status()
    return response.json()

def generar_datos_weekend(cadena, mercados, tipo):
    if cadena not in CADENA_URLS:
        raise ValueError("Cadena no válida (BK o MC).")

    if tipo not in TIPOS:
        raise ValueError("Tipo de weekendDays no válido.")

    weekendays = TIPOS[tipo]
    datos = obtener_datos_desde_api(cadena)

    filtrados = []
    for item in datos:
        if item.get("Pais") in mercados:
            item["FinesDeSemana"] = weekendays
            filtrados.append(item)

    return json.dumps(filtrados, ensure_ascii=False, indent=4)

