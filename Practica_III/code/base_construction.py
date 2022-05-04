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




















