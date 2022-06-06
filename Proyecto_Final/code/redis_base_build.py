import redis
import pandas as pd
from datetime import datetime
import redis_queries as db_redis
db = redis.Redis(host='127.0.0.1', port=6379, db=0, charset="utf-8", decode_responses=True)
db.flushdb()
gastosG= pd.read_csv('data/GastosExtra.csv')
ingresosi= pd.read_csv('data/IngresosExtra.csv')

def carga_datosPrueba(pruebasG, pruebasI):
    key1G='gastoExtra:Gasto:'
    key2G='gastoExtra:Concepto:'
    key3G='gastoExtra:Hora:'
    key4G='gastoExtra:Usuario:'

    key1I='ingresoExtra:Ingreso:'
    key2I='ingresoExtra:Concepto:'
    key3I='ingresoExtra:Hora:'
    key4I='ingresoExtra:Usuario:'
    for index, row in pruebasG.iterrows():
        db.rpush(key1G, row[2])
        db.rpush(key2G, row[1])
        db.rpush(key3G, row[0])
        db.rpush(key4G, row[3])
        
    for index, row in pruebasI.iterrows():
        db.rpush(key1I, row[2])
        db.rpush(key2I, row[1])
        db.rpush(key3I, row[0])
        db.rpush(key4I, row[3])


carga_datosPrueba(gastosG, ingresosi)
