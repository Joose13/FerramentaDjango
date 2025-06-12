from datetime import datetime, timedelta
import re
import json
import requests

requests.packages.urllib3.disable_warnings()

def generar_json(gd_list, utc_offset, opcion, fechas):
    datetime_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$|^null$"
    new_record_list = []

    for bloque in fechas:
        init = bloque['init']
        end = bloque['end']
        offset = bloque['offset']

        if not re.match(datetime_regex, init) or not re.match(datetime_regex, end):
            raise ValueError("Formato de fecha inválido")

        init_date = None if init == "null" else datetime.strptime(init[:-1], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=utc_offset)
        end_date = None if end == "null" else datetime.strptime(end[:-1], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=utc_offset)

        record = {
            "fechaInicio": init_date.strftime("%Y-%m-%dT%H:%M:%SZ") if init_date else None,
            "fechaFin": end_date.strftime("%Y-%m-%dT%H:%M:%SZ") if end_date else None,
            "horaLimitePreparacion": "23:59:59",
            "habilitado": True,
            "horasPreparacion": offset
        }
        new_record_list.append(record)

    results = []

    for gd in gd_list:
        url = f"http://192.168.1.3:3000/api/grupos/{gd.strip()}"
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            continue

        data = response.json()
        if "fechaMaxPreparacion" in data and "1" in data["fechaMaxPreparacion"]:
            if "fechasPreparacionDefecto" in data["fechaMaxPreparacion"]["1"]:
                for index, record in enumerate(new_record_list):
                    data["fechaMaxPreparacion"]["1"]["fechasPreparacionDefecto"].insert(index, record)
                    if opcion == 1 and "2" in data["fechaMaxPreparacion"]:
                        data["fechaMaxPreparacion"]["2"]["fechasPreparacionDefecto"].insert(index, record)
                results.append(data)

    return results

