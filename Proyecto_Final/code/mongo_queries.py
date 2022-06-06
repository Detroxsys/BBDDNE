import pandas as pd
import numpy as np
from datetime import datetime
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

conn_str = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn_str,
                             server_api=ServerApi('1'),
                             serverSelectionTimeoutMS=5000)

# Probando conexión
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")


db = client['Tienda']
# Registro de una nueva orden
def nueva_orden(compra:list, fecha:datetime = datetime.now()):
    hora = fecha.strftime('%H:%M:%S')
    fecha = fecha.strftime('%Y-%m-%d')
    total_orden = sum([x[2] for x in compra])
    compra = [{'producto_id': x[0], 'cantidad': x[1], 'subtotal': x[2]} for x in compra]
    orden = {'fecha': fecha ,
             'hora' : hora, 
             'compra': compra,
             'total_orden': total_orden }
    orden_id = db.Ordenes.insert_one(orden).inserted_id
    return orden_id

# Registro de un nuevo pedido
def nuevo_pedido(fecha_entrega:datetime, nombre_cliente:str, telefono:str, compra:list, fecha_apertura:datetime = datetime.now()):
    hora_apertura = fecha_apertura.strftime('%H:%M:%S')
    fecha_apertura = fecha_apertura.strftime('%Y-%m-%d')
    hora_entrega = fecha_entrega.strftime('%H:%M:%S')
    fecha_entrega = fecha_entrega.strftime('%Y-%m-%d')
    total_orden = sum([x[2] for x in compra])
    compra = [{'producto_id': x[0], 'cantidad': x[1], 'subtotal': x[2]} for x in compra] 
    pedido = {'fecha_apertura': fecha_apertura ,
              'hora_apertura' : hora_apertura,
             'fecha_entrega': fecha_entrega,
             'hora_entrega' : hora_entrega,
             'nombre_cliente': nombre_cliente,
             'telefono': telefono,
             'compra': compra,
             'total_orden': total_orden }
    pedido_id = db.Pedidos.insert_one(pedido).inserted_id

    return pedido_id

# 1.Total de venta de órdenes por día:
def venta_ordenes_por_dia(fecha:datetime= datetime.now()): 
    fecha = fecha.strftime('%Y-%m-%d')
    total = db.Ordenes.aggregate([{ "$match": { "fecha": fecha}},
                                  { "$group": { "_id": "$fecha", "total_dia" : {'$sum': '$total_orden'} }},
                                   { "$project": { "_id":0, "total_dia" : 1 }}])
    res = []                     
    for t in total:
        res.append(t)
    return res[0]

# 2. Consultar pedidos por fecha de entrega
def consultar_entregas(fecha_entrega:datetime = datetime.today(), format:bool=True):
    fecha_entrega = fecha_entrega.strftime('%Y-%m-%d')
    resultado = db.Pedidos.find({ "fecha_entrega": fecha_entrega}).sort('hora_entrega')
    
    if format:
        df = pd.DataFrame()
        for p in resultado:
            l = []
            for prod in p['compra']:
                l.append('{} : {}'.format(prod['producto_id'], prod['cantidad']))
            columna = []
            columna.append('Hora: {}'.format(p['hora_entrega']))
            columna.append('Tel: {}'.format(p['telefono']))
            total = "${:,}".format(p['total_orden'])
            columna.append('Total: {}'.format(total))
            columna = columna + l
            df = pd.concat([df, pd.DataFrame(columna, columns = [p['nombre_cliente']])], axis=1)
            #df[p['nombre_cliente']] = columna
        df = df.fillna('')
        return df

    pedidos = []
    for p in resultado:
        pedidos.append(p)
    return pedidos


# 3. Total de pagos de anticipos por día
def pago_anticipos_por_dia(fecha_apertura:datetime = datetime.today()):
    fecha_apertura = fecha_apertura.strftime('%Y-%m-%d')
    total = db.Pedidos.aggregate([{ "$match": { "fecha_apertura": fecha_apertura}},
                                   { "$group": { "_id": "$fecha_apertura", "total_anticipos_dia" : {'$sum': '$total_orden'} }},
                                   { "$project": { "_id":0, "total_anticipos_dia" : 1 }}])
    res = []                     
    for t in total:
        res.append(t)
    print(res)
    return res[0]['total_anticipos_dia']*0.5


# 4. Total de pagos de entregas por día
def pago_entregas_por_dia(fecha_entrega:datetime = datetime.today()):
    fecha_entrega = fecha_entrega.strftime('%Y-%m-%d')
    total = db.Pedidos.aggregate([{ "$match": { "fecha_entrega": fecha_entrega}},
                                   { "$group": { "_id": "fecha_entrega", "total_pago_entregas" : {'$sum': '$total_orden'} }},
                                   { "$project": { "_id":0, "total_pago_entregas" : 1 }}])
    res = []                     
    for t in total:
        res.append(t)
    return res[0]['total_pago_entregas']*0.5


#5. Consultar cantidades de productos a entregar por día
def productos_para_entregas(fecha_entrega:datetime = datetime.today()):
    fecha_entrega = fecha_entrega.strftime('%Y-%m-%d')
    resultado = db.Pedidos.aggregate([{ "$match": { "fecha_entrega": fecha_entrega}},
                                      { "$unwind": "$compra" },
                                      { "$group": { "_id": "$compra.producto_id", "total_piezas" : {'$sum':'$compra.cantidad'} }},
                                      { "$project": { "_id":1, "total_piezas" : 1 }}])
    pedidos = []                     
    for p in resultado:
        pedidos.append(p)
    return pd.DataFrame(pedidos).sort_values('total_piezas', axis=0, ascending=False)



