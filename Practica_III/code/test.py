from email import message
from tkinter import* #pip install tk 
from tkinter import ttk
from PIL import Image, ImageTk  #pip install pillow
from tkinter import messagebox
import pandas as pd 
import numpy as np
from cassandra.cluster import Cluster
from pandastable import Table, TableModel 
from bson.objectid import ObjectId
import pymongo
from pymongo import GEOSPHERE
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta

#Alternativa:
# client = MongoClient('localhost', 27017)

# Carga de las estaciones
estaciones = pd.read_csv('data/estaciones.csv')
dict_id_estacion = dict(zip(estaciones.id, estaciones.name))
dict_estacion_id = dict(zip(estaciones.name, estaciones.id))

print(dict_estacion_id['Cadman Plaza E & Tillary St'])
print(dict_id_estacion[232])