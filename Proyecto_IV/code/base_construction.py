from neomodel import db, clear_neo4j_database
from neomodel import StructuredNode,  StructuredRel, RelationshipTo, RelationshipFrom
from neomodel import StringProperty, BooleanProperty, DateTimeProperty
import pandas as pd
from neomodel import clear_neo4j_database

db.set_connection('neo4j://neo4j:password@localhost:7687')
clear_neo4j_database(db)

class Compro(StructuredRel):
    tienda = StringProperty()
    fecha = StringProperty()

class Ofrece(StructuredRel):
    cumple = BooleanProperty()


class Estado(StructuredNode):
    estado = StringProperty(unique_index=True)
    tiendas = RelationshipTo('Tienda', 'CONTIENE')

class Categoria(StructuredNode):
    nombre = StringProperty(unique_index=True)

class Tienda(StructuredNode):
    nombre = StringProperty(unique_index=True)
    estado = RelationshipFrom('Estado', 'CONTIENE')
    ofrece = RelationshipTo('Producto', 'OFRECE', model=Ofrece)

class Producto(StructuredNode):
    nombre = StringProperty(unique_index=True)
    categoria = RelationshipTo('Categoria', 'ES_CATEGORIA')
    tiendas = RelationshipFrom('Tienda', 'OFRECE', model=Ofrece)

class Usuario(StructuredNode):
    nombre = StringProperty(unique_index=True)
    compra = RelationshipTo('Producto', 'COMPRA', model=Compro)




# Esta función carga nodos y relaciones. Tarda un poco en ejecutarse
def carga_de_datos():

    clear_neo4j_database(db)
    df = pd.read_csv('Tiendas_limpio.csv')
    df = df.head(1000)
    #Estados
    for i in df.ENTIDAD.unique():
        _ = Estado(estado = i).save()

    #Categorías
    for i in df['NORMA OFICIAL MEXICANA VERIFICADA'].unique():
        _ = Categoria(nombre = i).save()

    #Productos
    for i in df['TIPO DE PRODUCTO'].unique():
        _ = Producto(nombre = i).save()

    #Tiendas
    for i in df['RAZON SOCIAL VISITADA'].unique():
        TIENDA = Tienda(nombre = i).save()

        df_tienda = df[df['RAZON SOCIAL VISITADA'] == i]

        for i in range(len(df_tienda)):
            row = df_tienda.iloc[i]

            ESTADO = Estado.nodes.get(estado= row['ENTIDAD'])
            PRODUCTO = Producto.nodes.get(nombre= row['TIPO DE PRODUCTO'])
            CATEGORIA = Categoria.nodes.get(nombre= row['NORMA OFICIAL MEXICANA VERIFICADA'])

            ESTADO.tiendas.connect(TIENDA)
            TIENDA.ofrece.connect(PRODUCTO, {'cumple':row['CUMPLIO?'] })
            PRODUCTO.categoria.connect(CATEGORIA)

carga_de_datos()
print('Termine de cargar datos')