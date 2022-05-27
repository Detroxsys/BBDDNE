from neomodel import db
from neomodel import StructuredNode,  StructuredRel, RelationshipTo, RelationshipFrom
from neomodel import StringProperty, BooleanProperty, DateTimeProperty
from datetime import datetime
import pandas as pd
db.set_connection('neo4j://neo4j:password@localhost:7687')

class Ofrece(StructuredRel):
    cumple = BooleanProperty()


class Compro(StructuredRel):
    tienda = StringProperty()
    fecha = StringProperty()

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


#---------------------------------- Check if user exists --------------------------------
def CheckUser(usuario:str):
    resultado=True
    if not Usuario.nodes.get_or_none(nombre=usuario):
        resultado=False
    return(resultado)
#---------------------------------- Query Usuario Alta ----------------------------------
# Da de alta un usuario
def AltaUsuario(usuario:str):
    Usuario(nombre = usuario).save()

#---------------------------------- Query Estados ----------------------------------
# Devuelve todos los estados en una lista

def todos_estados():
    query = "MATCH (e:Estado) RETURN e"
    results, meta = db.cypher_query(query)

    estados = [Estado.inflate(row[0]).estado for row in results]
    return estados

#---------------------------------- Query Productos  ----------------------------------
# Devuelve todos los productos
def todos_productos():
    query = "MATCH (p:Producto) RETURN p"
    results, meta = db.cypher_query(query)

    productos = [Producto.inflate(row[0]).nombre for row in results]
    return productos


#---------------------------------- Query Tiendas en estado ----------------------------------
# Devuelve todas las tiendas en un estado
def tiendas_en_estado(estado:str):
    query = "MATCH (e:Estado {estado:'"+ estado+"'}) -[CONTIENE]-> (t:Tienda) RETURN t"
    results, meta = db.cypher_query(query)

    tiendas = [Tienda.inflate(row[0]).nombre for row in results]
    return tiendas

#---------------------------------- Query Productos en Tienda ----------------------------------
# Devuelve todos los productos en una tienda
def productos_en_tienda(tienda:str):
    query = "MATCH (t:Tienda {nombre:'"+ tienda+"'}) -[OFRECE]-> (p:Producto) RETURN p"
    results, meta = db.cypher_query(query)

    productos = [Producto.inflate(row[0]).nombre for row in results]
    return productos


#---------------------------------- Query 1 ----------------------------------
# Dado un estado y producto, buscar lugares donde se pueda encontrar

def q1_hallar_tienda(estado:str, producto:str):
    query = "MATCH (e:Estado {estado:'" + estado + "'}) -[CONTIENE]-> (t:Tienda) -[OFRECE]-> (p:Producto {nombre:'" + producto + "'}) RETURN t"
    results, meta = db.cypher_query(query)

    tiendas = [Tienda.inflate(row[0]).nombre for row in results]
    return tiendas

#---------------------------------- Query 2 ----------------------------------
# Dado un estado y tienda, verificar si tiene algún incumplimiento
def q2_incumplimientos(estado:str, tienda:str):
    query = "MATCH (e:Estado {estado:'" + estado + "'}) -[CONTIENE]-> (t:Tienda{nombre:'" + tienda + "'}) -[OFRECE{cumple:FALSE}]-> (p:Producto) RETURN p"
    results, meta = db.cypher_query(query)

    productos = [Producto.inflate(row[0]).nombre for row in results]
    return productos

#---------------------------------- Query 3 ----------------------------------
# Dado un estado y producto, buscar alternativas sin incumplimiento
def q3_alternativas(estado:str, producto:str):
    query = "MATCH (e:Estado {estado:'"+ estado+"'}) -[CONTIENE]-> (t:Tienda) -[OFRECE{cumple:TRUE}]-> (p:Producto {nombre:'" + producto + "'}) RETURN t"
    results, meta = db.cypher_query(query)

    tiendas = [Tienda.inflate(row[0]).nombre for row in results]
    return tiendas

#---------------------------------- Query 4 ----------------------------------
# Dado un estado y producto, buscar alternativas sin incumplimiento
def q4_comprar(usuario:str, producto:str, tienda:str):
    fecha=datetime.now()
    fecha2 = str(fecha.strftime("%d/%m/%Y %H:%M:%S"))
    prod=Producto.nodes.get(nombre=producto)
    Usuario.nodes.get(nombre=usuario).compra.connect(prod, {'tienda':tienda, 'fecha': fecha2})


#---------------------------------- Query 5 ----------------------------------
def q5_registros(usuario:str):
    query="MATCH (:Usuario {nombre: '"+usuario+"'})-[r]-(s) RETURN {fecha: r.fecha, producto:s.nombre, tienda:r.tienda}"
    results=db.cypher_query(query)
    output = pd.DataFrame()
    resultados=[]
    for result in results[0]:
        resultados.append(result[0])
    return pd.DataFrame(resultados)

#---------------------------------- Query 6 ----------------------------------
def q7_recomendar(producto:str):
    query = "MATCH (Producto {nombre:'" + producto + "'}) -[ES_CATEGORIA]-> (c:Categoria)  RETURN c"
    results, meta = db.cypher_query(query)
    cats = [Categoria.inflate(row[0]).nombre for row in results]

    productos_lista = []

    for cat in cats:

        query = "MATCH (Producto {nombre:'" + producto + "'}) <-[COMPRO]- (u:Usuario) RETURN u"
        results, meta = db.cypher_query(query)
        usuarios = [Usuario.inflate(row[0]).nombre for row in results]

        for user in usuarios:
            query = "MATCH (u:Usuario{nombre:'"+user+"'}) -[COMPRO]->(p:Producto) -[ES_CATEGORIA]-> (Categoria{nombre:'" + cat+"'}) RETURN p"
            results, meta = db.cypher_query(query) 
            productos = [Producto.inflate(row[0]).nombre for row in results]
            productos_lista += productos

        productos_lista = list(set(productos_lista))

    return productos_lista
#---------------------------------- Query 8 ----------------------------------
def q8_incumpliminetos():
    tiendas="Match (e:Estado)-[CONTIENE]-> (t) RETURN  e, count(*)"
    incumplimientos="Match (e:Estado)-[CONTIENE]-> (t) -[Ofrece {cumple:False}]->(p) RETURN  e, count(distinct(t))"
    tiendas, meta= db.cypher_query(tiendas)
    incumplimientos, meta= db.cypher_query(incumplimientos)

    resultado1 = pd.DataFrame([{'estado':Estado.inflate(row[0]).estado, 'tiendas':row[1]} for row in tiendas])
    resultado2 = pd.DataFrame([{'estado':Estado.inflate(row[0]).estado, 'incumplimientos':row[1]} for row in incumplimientos])
    res=resultado1.join(resultado2.set_index('estado'), on='estado')
    res['Tasa de incumplimiento']=res['incumplimientos']/res['tiendas']
    res=res.sort_values(['Tasa de incumplimiento'], ascending=False).reset_index(drop=True)
    return(res)
