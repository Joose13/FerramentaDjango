from decouple import config
import mysql.connector

def contar_pedidos(localizaciones_input, conexion):
    db_connections = {
        "BK": {
            "host": config("BK_DB_HOST"),
            "user": config("BK_DB_USER"),
            "password": config("BK_DB_PASSWORD"),
            "database": config("BK_DB_NAME")
        },
        "MC": {
            "host": config("MC_DB_HOST"),
            "user": config("MC_DB_USER"),
            "password": config("MC_DB_PASSWORD"),
            "database": config("MC_DB_NAME")
        }
    }

    conn_info = db_connections[conexion]
    total_pedidos = 0

    try:
        localizaciones = localizaciones_input.split(",")

        for localizacion in localizaciones:
            conn = mysql.connector.connect(**conn_info)
            cursor = conn.cursor()

            query = """
                SELECT COUNT(*) FROM Pedidos
                WHERE id_tienda = %s
                AND estado = "RECIBIDO"
            """
            cursor.execute(query, (localizacion.strip(),))
            count = cursor.fetchone()[0]
            total_pedidos += count

            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error al consultar la base de datos: {str(e)}")

    return total_pedidos

