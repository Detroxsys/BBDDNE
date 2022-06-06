import redis_queries as db_redis 
import pandas as pd 
db_redis0 = db_redis.RDB()

pruebasG = pd.read_csv('data/GastosExtra.csv')
pruebasI = pd.read_csv('data/IngresosExtra.csv')
#print(pruebasG)
def carga_datosPureba(db_redis0, pruebasG, pruebasI):
    key1G='gastoExtra:Gasto:'
    key2G='gastoExtra:Concepto:'
    key3G='gastoExtra:Hora:'
    key4G='gastoExtra:Usuario:'

    key1I='ingresoExtra:Ingreso:'
    key2I='ingresoExtra:Concepto:'
    key3I='ingresoExtra:Hora:'
    key4I='ingresoExtra:Usuario:'
    for index, row in pruebasG.iterrows():
        db_redis0.db.rpush(key1G, row[2])
        db_redis0.db.rpush(key2G, row[1])
        db_redis0.db.rpush(key3G, row[0].strftime("%Y-%m-%d %H:%M:%S"))
        db_redis0.db.rpush(key4G, row[3])

    for index, row in pruebasI.iterrows():
        db_redis0.db.rpush(key1I, row[2])
        db_redis0.db.rpush(key2I, row[1])
        db_redis0.db.rpush(key3I, row[0].strftime("%Y-%m-%d %H:%M:%S"))
        db_redis0.db.rpush(key4I, row[3])

carga_datosPureba(db_redis0, pruebasG, pruebasI)

print(db_redis0.dfGastosExtra())

