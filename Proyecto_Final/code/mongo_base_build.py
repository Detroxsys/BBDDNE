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


# Borrar base y volver a crear
client.drop_database('Tienda')

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


def precarga_ordenes():
    compras  = [[['Volovan Jamon', 3, 45], ['Volovan Pollo', 1, 15], ['Volovan Fresa', 2, 30]],
                [['Volovan Choriqueso', 1, 15], ['Volovan Zarzamora', 1, 15], ['Volovan Manjar', 1, 15]],
                [['Volovan Jamon', 2, 30], ['Volovan Piñacoco', 1, 15], ['Volovan Cajeta', 1, 15]],
                [['Volovan Pastor', 2, 36], ['Volovan Choriqueso', 1, 15], ['MiniVolovan Tres quesos', 2, 16]],
                [['MiniVolovan Nutella', 2, 16], ['MiniVolovan Zarzamora', 1, 8], ['MiniVolovan Cajeta', 3, 24]],
                [['Volovan Jamon', 4, 60], ['Volovan Pollo', 4, 60]],
                [['Volovan Zarzamora', 3, 45], ['Volovan Piña', 2, 30]],
                [['Volovan Tres quesos', 2, 30], ['Volovan Champiñones', 2, 30]],
                [['Volovan Champiñones', 5, 75], ['Volovan Pastor', 1, 18]],
                [['Volovan Nutella', 1, 15], ['MiniVolovan Fresa', 1, 8]],
                [['Princesa', 3, 60]],
                [['MegaVolo', 4, 80]],
                [['Reyna', 1, 40]],
                [['Reyna', 1, 40]],
                [['MisterVolo', 1, 50]] ]

    for c in compras:
        nueva_orden(c)
    return

def precarga_pedidos():
    compras  = [[['Volovan Jamon', 10, 150], ['Volovan Pollo', 10, 150], ['Volovan Fresa', 10, 150]],
                [['Volovan Jamon', 20, 300], ['Volovan Pollo', 10, 150], ['Volovan Fresa', 10, 150]],
                [['Volovan Choriqueso', 15, 225], ['Volovan Zarzamora', 15, 225], ['Volovan Manjar', 10, 150]],
                [['Volovan Jamon', 15, 225], ['Volovan Piñacoco', 10, 150], ['Volovan Cajeta', 10, 150]],
                [['Volovan Jamon', 10, 150], ['Volovan Piñacoco', 10, 150], ['Volovan Cajeta', 10, 150]],
                [['Volovan Jamon', 30, 450], ['Volovan Pollo', 30, 450]],
                [['Volovan Zarzamora', 35, 525], ['Volovan Piña', 20, 300]],
                [['Volovan Zarzamora', 20, 300], ['Volovan Piña', 20, 300]],
                [['Volovan Tres quesos', 20, 300], ['Volovan Champiñones', 20, 300]],
                [['Volovan Tres quesos', 20, 300], ['Volovan Champiñones', 12, 180]],
                [['Princesa', 30, 600]],
                [['MegaVolo', 40, 800]],
                [['Reyna', 10, 400]],
                [['Reyna', 15, 600]],
                [['MisterVolo', 25, 1250]] ]

    nombres = ['Marcela Cruz', 'Victor Almendra', 'Yeudiel Lara', 'Pablo Castillo', 'Pamela Larios',
                'Diego Cardenas', 'Adan Medrano', 'Ximena Robles', 'Lionel Messi', 'Luis Perales',
                'Rita Jimenez', 'Alejandro Pimentel', 'Leo Martinez', 'Oscar Sanchez', 'Ana Meda']
                
    telefonos = ['524875475','923550340','056241059','256743290','100456580',
                 '511136342','748412841','339374033','982005739','673425710',
                 '031079473','827037601','074426997','884081039','186980650']
                 
    fechas_str =  ['2022-06-10 12:30:00', '2022-06-09 11:35:00', '2022-06-10 16:45:00',
               '2022-06-08 15:20:00', '2022-06-15 09:15:00', '2022-06-15 08:00:00',
               '2022-06-14 10:15:00', '2022-06-29 11:20:00', '2022-06-08 10:00:00',
               '2022-06-08 12:45:00', '2022-06-09 13:45:00', '2022-06-11 14:00:00',
               '2022-06-12 09:15:00', '2022-06-12 10:15:00', '2022-06-08 12:00:00']

    fechas = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in fechas_str ]

    for i in range(15):
        nuevo_pedido(fechas[i],nombres[i], telefonos[i], compras[i])
    return


precarga_ordenes()
precarga_pedidos()

print("Base Mongo Cargada")