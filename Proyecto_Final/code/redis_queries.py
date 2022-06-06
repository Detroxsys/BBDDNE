import redis
import pandas as pd
from datetime import datetime

db = redis.Redis(host='127.0.0.1', port=6379, db=0, charset="utf-8", decode_responses=True)

def carga_productos(restantes):
    for index, row in restantes.iterrows():
        key= 'Productos:'+row[0]
        result= db.set(key, int(row[1]))
    return result

def get_sobrantes(producto):
    key="Productos:"+producto
    result = db.get(key)
    return int(result)

def producidos(producto, producido):
    key="Productos:"+producto
    result= db.set(key, get_sobrantes(producto)+producido)
    return result

def comprados(producto, comprado):
    key="Productos:"+producto
    result= db.set(key, get_sobrantes(producto)-comprado)
    return result

def gastosExtra(gastado, concepto, user):
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key1='gastoExtra:Gasto:'
    key2='gastoExtra:Concepto:'
    key3='gastoExtra:Hora:'
    key4='gastoExtra:Usuario:'
    db.rpush(key1, gastado)
    db.rpush(key2, concepto)
    db.rpush(key3, hora)
    db.rpush(key4, user)
    return 

def gastosExtraTotales():
    gastos= db.lrange('gastoExtra:Gasto:', 0, -1)
    return sum(map(float, gastos))

def ingresosExtra(ingresado, concepto, user):
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key1='ingresoExtra:Ingreso:'
    key2='ingresoExtra:Concepto:'
    key3='ingresoExtra:Hora:'
    key4='ingresoExtra:Usuario:'
    db.rpush(key1, ingresado)
    db.rpush(key2, concepto)
    db.rpush(key3, hora)
    db.rpush(key4, user)
    return

def ingresosExtraTotales():
    gastos= db.lrange('ingresoExtra:Ingreso:', 0, -1)
    return sum(map(float, gastos))

def dfIngresosExtra():
        tiempos=[]
        for i in db.lrange('ingresoExtra:Hora:', 0, -1):
            tiempos.append(datetime.strptime(i, "%Y-%m-%d %H:%M:%S"))
        ingdict={'Fecha': tiempos, 'Concepto':db.lrange('ingresoExtra:Concepto:', 0, -1), \
            'Ingreso': db.lrange('ingresoExtra:Ingreso:', 0, -1), 'Usuario': db.lrange('ingresoExtra:Usuario:', 0, -1)}
        ingdf=pd.DataFrame.from_dict(data=ingdict)
        return( ingdf)

def dfGastosExtra():
        tiempos=[]
        for i in db.lrange('gastoExtra:Hora:', 0, -1):
            tiempos.append(datetime.strptime(i, "%Y-%m-%d %H:%M:%S"))
        gastdict= {'Fecha': tiempos, 'Concepto':db.lrange('gastoExtra:Concepto:', 0, -1), \
            'Costo': db.lrange('gastoExtra:Gasto:', 0, -1), 'Usuario': db.lrange('gastoExtra:Usuario:', 0, -1)}
        gastodf=pd.DataFrame.from_dict(data=gastdict)
        return(gastodf)


