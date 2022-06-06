import mongo_queries as db_mongo
from datetime import datetime
hoy = datetime.now()

print(db_mongo.venta_ordenes_por_dia(hoy))
