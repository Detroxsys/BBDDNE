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
db = client['BDBicis']

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
# Dar de alta usuario: crear_usuario()

# Verificar si usuario existe
def existe_usuario(usuario:str):
    existe = db.Usuarios.find_one({'nombre_usuario': usuario})
    if existe:
        return existe['_id']
    else:
        return False

# Regresa lista de lugares guardados del usuario
def lugares_guardados(usuario:str):
    respuesta = db.Usuarios.find_one({'nombre_usuario': usuario}, {'lugares':1})
    lugares_guardados = []
    for lugar in respuesta['lugares']:
        nombre = lugar['nombre_lugar']
        coordenadas = lugar['ubicacion']['coordinates']
        lugares_guardados.append((nombre, coordenadas))

    return lugares_guardados

def lugares_guardados_nombres(usuario:str):
    respuesta = db.Usuarios.aggregate([{ "$unwind": "$lugares" },
                                    { "$match": { "nombre_usuario": usuario}},
                                    { "$project": { "_id":0, "lugares.nombre_lugar" : 1 }}])
    lugares = []
    for res in respuesta:
        lugares.append(res['lugares']['nombre_lugar'])
    return lugares

# Determina si un nombre de lugar ya ha sido ocupado por ese usuario
def existe_lugar(usuario:str, nombre_lugar:str):
    existe = db.Usuarios.find_one({'nombre_usuario': usuario, 'lugares.nombre_lugar':nombre_lugar})
    if existe:
        return existe['lugares'][0]['ubicacion']['coordinates']
    return False


# Añade un nuevo lugar, si es que este no existe
def nuevo_lugar(usuario:str, nombre_lugar:str, longitud_lugar, latitud_lugar):
    existe = db.Usuarios.find_one({'nombre_usuario': usuario, 'lugares.nombre_lugar':nombre_lugar})
    if existe:
        return 0

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
    
    lugares = db.Usuarios.find_one({'nombre_usuario':usuario})['lugares']

    nuevo_lugar = {'nombre_lugar': nombre_lugar,
                    'ubicacion': {'type': "point", 
                                        'coordinates' : [longitud_lugar, latitud_lugar]},
                    'estaciones': estaciones_mas_cercanas}
    
    lugares.append(nuevo_lugar)

    db.Usuarios.update_one({'nombre_usuario':usuario}, {'$set':{'lugares': lugares}})
    return True


# Estaciones más cercanas a un lugar guardado
def estaciones_mas_cercanas(usuario:str, nombre_lugar:str):
    existe = db.Usuarios.aggregate([{ "$unwind": "$lugares" },
                                    { "$match": { "nombre_usuario": usuario, 'lugares.nombre_lugar':nombre_lugar}},
                                    { "$project": { "_id":0, "lugares.estaciones" : 1 }}])
    respuesta = []
    for est in existe:
        respuesta.append(est)
    if respuesta:
        respuesta = respuesta[0]['lugares']['estaciones']
        for est in respuesta:
            est['longitud'] = est['ubicacion']['coordinates'][0]
            est['latitud'] = est['ubicacion']['coordinates'][1]
        df = pd.DataFrame(respuesta)
        df = df[['_id', 'nombre_estacion', 'longitud', 'latitud']]
        return df
    return None

##################################################################################################################################
# Estaciones más cercanas a una ubicación cualquiera
def estaciones_mas_cercanas_loc(longitud:float, latitud:float, limit:int=3):
    estaciones = db.Estaciones.aggregate([
    { 
        "$geoNear": {
            "near": [ longitud , latitud],
            "distanceField": "distancia", 
            "maxDistance": 50000,
            "spherical": True
        }
    },
    {
        "$limit": limit
    }])
    estaciones_mas_cercanas = []
    for estacion in estaciones:
        estaciones_mas_cercanas.append(estacion)
    return estaciones_mas_cercanas

###############################################################################################################################
# Sugerir ruta dada estación y tiempo de viaje (en segundos)
def ruta_desde_estacion( id_origen:int, tiempo_viaje:int):
    respuesta = db.Rutas.find({'id_origen':id_origen,
                               'id_destino': {'$ne': id_origen},
                               'tiempo_promedio':{ '$gt': tiempo_viaje-3600, '$lt': tiempo_viaje+3600}})
    
    respuesta = pd.DataFrame(respuesta)

    if len(respuesta) == 0:
        return None
        
    respuesta['dif_tiempo'] = abs(respuesta['tiempo_promedio'] - tiempo_viaje )
    respuesta =  respuesta.sort_values(by='dif_tiempo')

    return respuesta.head(3)
        
##################################################################################################################################
# Viaje redondo
def viaje_redondo(id_origen:int, tiempo_viaje:int):
    
    viaje_ida = db.Rutas.find({'id_origen':id_origen,
                               'id_destino': {'$ne': id_origen}})
    viaje_vuelta = db.Rutas.find({'id_origen':{'$ne': id_origen},
                               'id_destino': id_origen})
    
    viaje_ida = pd.DataFrame(viaje_ida)[['id_origen', 'id_destino', 'tiempo_promedio']]
    viaje_ida.columns = ['origen', 'punto_medio', 'tiempo_ida']

    viaje_vuelta = pd.DataFrame(viaje_vuelta)[['id_origen','id_destino','tiempo_promedio']]
    viaje_vuelta.columns = ['punto_medio', 'destino', 'tiempo_vuelta']
    
    viaje_redondo = viaje_ida.merge(right=viaje_vuelta, how='inner', on='punto_medio')
    viaje_redondo['tiempo_promedio'] = viaje_redondo['tiempo_ida'] + viaje_redondo['tiempo_vuelta']

    viaje_redondo['dif_tiempo'] = abs(viaje_redondo['tiempo_promedio'] - tiempo_viaje )
    viaje_redondo =  viaje_redondo.sort_values(by='dif_tiempo')

    return viaje_redondo.head(3)

#########################################################################################################################
#Actualizar datos
def actualizar_tiempo(origen_id:int, destino_id:int, tiempo:float):
    ra = db.Rutas.find({'id_origen':origen_id,
                                'id_destino':destino_id},{'tiempo_promedio':1, 'registros':1})
    
    ra=ra[0] #qué pasa si no existe la ruta? qué se guarda en ra?
    if ra:
        nuevotiempo= ((ra['tiempo_promedio']*ra['registros'])+tiempo)/(ra['registros']+1)
        db.Rutas.update_one({'_id':ra['_id']}, {'$set': {'tiempo_promedio':  nuevotiempo, 'registros':ra['registros']+1}})
        return ()
    else:
        carga_ruta(origen_id, destino_id, tiempo, 1)

#Consultar viajes realizados
def historial_viajes(usuario:str):
    viajes = db.Viajes.find({'nombre_usuario': usuario})
    return pd.DataFrame(viajes)

################################################################################





