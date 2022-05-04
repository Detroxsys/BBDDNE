import pandas as pd
import numpy as np
import datetime
import pprint
from bson.objectid import ObjectId
import pymongo
from pymongo import GEOSPHERE
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# es importante mapear al puerto usando -p 27017:27017 al construir el contenedor o en el docker-compose.yml
conn_str = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn_str, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

#Alternativa:
# client = MongoClient('localhost', 27017)

# Probando conexión
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")


# Colección: Estaciones
# Estamos usando id propios
def carga_estacion( id:int, nombre:str, longitud, latitud):
    exists = db.Estaciones.find_one({'_id': id})
    if exists:
        return 0

    estacion = {'_id': id,
                'nombre_estacion': nombre,
                'ubicacion': {'type': "point", 'coordinates' : [longitud, latitud]}}
    
    estacion_id = db.Estaciones.insert_one(estacion).inserted_id

    return estacion_id

# Colección: Rutas
def carga_ruta( origen_id:int, destino_id:int, tiempo_promedio:float, registros:int):
    
    exists = db.Rutas.find_one({'id_origen': origen_id, 'id_destino': destino_id})
    if exists:
        return 0
    
    ruta = {'id_origen': origen_id,
            'id_destino': destino_id,
            'tiempo_promedio': tiempo_promedio,
            'registros': registros}

    ruta_id = db.Rutas.insert_one(ruta).inserted_id

    return ruta_id

# Colección: Viajes
def carga_viaje( origen_id:int, destino_id:int, salida:datetime, llegada:datetime, usuario):
    duracion = (llegada - salida).seconds
    viaje = {'id_origen': origen_id,
             'id_destino': destino_id,
             'hora_salida': salida,
             'hora_llegada': llegada,
             'duracion': duracion,
             'usuario': usuario}
    
    viaje_id = db.Viajes.insert_one(viaje).inserted_id
    
    return viaje_id

# Colección: Usuarios
def crear_usuario( nombre:str, nombre_lugar:str, longitud_lugar, latitud_lugar):
    existe = db.Usuarios.find_one({'nombre_usuario': nombre})
    if existe:
        return existe['_id']

    estaciones = db.Estaciones.aggregate([
    { 
        "$geoNear": {
            "near": [ longitud_lugar , latitud_lugar],
            "distanceField": "distancia", 
            "maxDistance": 50000,
            "spherical": True
        }
    },
    {
        "$limit": 3 
    }])
    estaciones_mas_cercanas = []
    for estacion in estaciones:
        estaciones_mas_cercanas.append(estacion)

    usuario = {'nombre_usuario' : nombre,
               'lugares': [{'nombre_lugar': nombre_lugar,
                           'ubicacion': {'type': "point", 
                                        'coordinates' : [longitud_lugar, latitud_lugar]},
                           'estaciones': estaciones_mas_cercanas}]
                }
    
    usuario_id = db.Usuarios.insert_one(usuario).inserted_id
    return usuario_id

##################################################################################################################################
# Borrar base y volver a crear
client.drop_database('BDBicis')
print("Se esta ejecutando el drop")
db = client['BDBicis']


# Carga de las estaciones
estaciones = pd.read_csv('data/estaciones.csv')
db.Estaciones.insert_many([{'_id': est[0],
                            'nombre_estacion': est[1],
                            'ubicacion': {'type': "point", 
                                          'coordinates' : [est[2], est[3]]}} for est in estaciones.values])

db.Estaciones.create_index( [("ubicacion.coordinates", pymongo.GEOSPHERE)] ) 


# Carga de las rutas con tiempo promedio
rutas = pd.read_csv('data/viajes.csv')
db.Rutas.insert_many([{'id_origen': ruta[0], 
                       'id_destino': ruta[1], 
                       'tiempo_promedio':ruta[2], 
                       'registros':ruta[3]} for ruta in rutas.values])


print('Implementación de base terminada')




















