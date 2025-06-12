import pymongo
from decouple import config

def contar_pedidos_iop(store_ids, conn):
    db_connections = {
        "BK": {
            "conn_str": config("MONGO_BK_CONN_STR"),
            "db_name": config("MONGO_BK_DB")
        },
        "MC": {
            "conn_str": config("MONGO_MC_CONN_STR"),
            "db_name": config("MONGO_MC_DB")
        }
    }

    conn_str = db_connections[conn]["conn_str"]
    client = pymongo.MongoClient(conn_str)
    db = client[db_connections[conn]["db_name"]]
    orders = db.pedidos

    store_ids_list = [int(s.strip()) for s in store_ids.split(",")]
    total_pedidos = 0

    for store_id in store_ids_list:
        pipeline = [
            {"$match": {"id": store_id, "estado": {"$nin": ["ANULADO", "FINALIZADO"]}}},
            {"$group": {"_id": None, "total": {"$sum": 1}}}
        ]
        result = list(orders.aggregate(pipeline))
        if result:
            total_pedidos += result[0]["total"]

    return total_pedidos

