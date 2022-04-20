import pandas as pd
import numpy as np
from tqdm import tqdm
from cassandra.cluster import Cluster

#####################################################################################################################################
#Conexion al cluster
#Es importante haber mapeado el puerto usando -p 9042:9042 al crear el contenedor
cluster = Cluster(['127.0.0.1'], port=9042)
#session = cluster.connect('bdnosql') #El keyspace lo creé desde la terminal

session = cluster.connect()

session.execute(
    """
    DROP KEYSPACE IF EXISTS bd_libros;
    """
)
#####################################################################################################################################
# Creación de keyspace y tablas
# Creación del keyspace
session.execute(
    """
    CREATE KEYSPACE bd_libros 
    WITH replication = {'class' : 'SimpleStrategy', 'replication_factor':1};
    """
)
session.set_keyspace('bd_libros')


### Creación de las tablas

# LIBROS POR CLIENTE (Queries 1,2,3)
session.execute(
    """
    CREATE TABLE libros_por_cliente (
    id_cliente text,
    titulo_libro text,
    autor_libro text,
    categoria text,
    calificacion int,
    nombre_cliente text STATIC,
    pais text STATIC,
    membresia text STATIC,
    PRIMARY KEY(id_cliente, titulo_libro, autor_libro)
    );
    """
)

## CATEGORIAS POR CLIENTE
#session.execute(
#    """
#    CREATE MATERIALIZED VIEW categorias_por_cliente AS
#    SELECT id_cliente, categoria, titulo_libro, autor_libro, calificacion
#    FROM libros_por_cliente
#    WHERE categoria IS NOT NULL
#    AND titulo_libro IS NOT NULL
#    AND autor_libro IS NOT NULL
#    PRIMARY KEY(id_cliente, categoria, titulo_libro, autor_libro);
#    """
#)

#CATEGORIAS POR CLIENTE
session.execute(
    """
    CREATE TABLE categorias_por_cliente(
    id_cliente text,    
    categoria text,
    titulo_libro text,
    autor_libro text,
    calificacion int,
    PRIMARY KEY(id_cliente,categoria, titulo_libro, autor_libro, calificacion)
    );
    """
)


# CLIENTES POR LIBRO (Query 4)
session.execute(
    """
    CREATE TABLE clientes_por_libro (
    titulo_libro text,
    autor_libro text,
    calificacion int,
    id_cliente text,
    categoria text,
    PRIMARY KEY((titulo_libro, autor_libro), calificacion, id_cliente)
    );
    """
)


# LIBROS POR CATEGORIA (Query 5)
session.execute(
    """
    CREATE TABLE libros_por_categoria (
    categoria text,
    titulo_libro text,
    autor_libro text,
    calificacion_promedio float,
    PRIMARY KEY (categoria, titulo_libro, autor_libro, calificacion_promedio)
    );
    """
)
session.execute(
    """
    CREATE INDEX ON libros_por_categoria(calificacion_promedio)"""
)

####################################################################################################################################
#QUERIES FUNCIONALES 
def Q0_check_usuario(id_cliente:str):
    existe_usuario = session.execute(
        """
        SELECT * FROM libros_por_cliente
        WHERE id_cliente = %s
        LIMIT 1
        """,
        [id_cliente]
    )
    if existe_usuario: 
        return True
    else: 
        return False

def Q1_alta_usuario(id_cliente:str, nombre_cliente:str, pais:str, membresia:str):
    existe_usuario = session.execute(
        """
        SELECT * FROM libros_por_cliente
        WHERE id_cliente = %s
        LIMIT 1
        """,
        [id_cliente]
    )

    if existe_usuario:
        return None

    session.execute(
        """
        INSERT INTO libros_por_cliente
        (id_cliente, nombre_cliente, pais, membresia)
        VALUES (%s, %s, %s, %s)
        """,
        (id_cliente, nombre_cliente, pais, membresia)
    )
    return 

def Q2_agregar_calificacion(id_cliente:str , titulo_libro:str, autor_libro:str, categoria:str, calificacion:int):
    existe_calif= session.execute(
        """
        SELECT categoria, calificacion FROM libros_por_cliente
        WHERE id_cliente=%s AND titulo_libro=%s  AND autor_libro=%s
        LIMIT 1
        """,
        [id_cliente, titulo_libro, autor_libro]
    )
    info_previa = existe_calif.one()
    
    if existe_calif:
        # pedir a usuario confirma que desea cambiar la calificación
        confirmacion_del_usuario = 1 #respuesta del usuario
        if not confirmacion_del_usuario:
            return

        info_previa = existe_calif.one()
        
        #Borrar la calificación anterior
        session.execute(
            """
            DELETE FROM clientes_por_libro
            WHERE titulo_libro=%s
            AND autor_libro=%s
            AND calificacion=%s
            AND id_cliente=%s
            """,
            (titulo_libro, autor_libro, info_previa.calificacion, id_cliente)
        )
        session.execute(
            """
            DELETE FROM categorias_por_cliente
            WHERE id_cliente=%s 
            AND categoria=%s
            AND titulo_libro=%s
            AND autor_libro=%s
            AND calificacion=%s
            """,
            (id_cliente, info_previa.categoria, titulo_libro, autor_libro, info_previa.calificacion)
        )
        

    #Agregar la nueva calificación
    session.execute(
        """
        INSERT INTO libros_por_cliente 
        (id_cliente, titulo_libro, autor_libro, categoria, calificacion)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (id_cliente, titulo_libro, autor_libro, categoria, calificacion)
    )
    session.execute(
        """
        INSERT INTO clientes_por_libro 
        (titulo_libro, autor_libro, id_cliente, calificacion, categoria)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (titulo_libro, autor_libro, id_cliente, calificacion, categoria)
    )
    session.execute(
        """
        INSERT INTO categorias_por_cliente 
        (id_cliente, titulo_libro, autor_libro, categoria, calificacion)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (id_cliente, titulo_libro, autor_libro, categoria, calificacion)
    )
    

    #Actualizar calificaciones promedio
    calificacion_promedio = session.execute(
        """
        SELECT AVG(calificacion) FROM clientes_por_libro
        WHERE titulo_libro=%s
        AND autor_libro=%s
        """,
        (titulo_libro, autor_libro)
    )
    calificacion_promedio = round(calificacion_promedio.one()[0], 2)

    categorias_del_libro = session.execute(
            """
            SELECT categoria FROM clientes_por_libro
            WHERE titulo_libro =%s
            AND autor_libro = %s
            """,
            (titulo_libro, autor_libro)
    )
    
    #En caso de que sea la única review que asigna esa categoría al libro y se cambie la categoría, necesitamos
    #eliminar la fila de la tabla libros_por_categoría
    if info_previa is not None:
        if  info_previa.categoria != categoria:
            unica_calificacion = True
    
            for row in categorias_del_libro:
                if row.categoria == info_previa.categoria: #entonces hay otras reviews que categorizan igual al libro
                    unica_calificacion = False
                session.execute(
                    """
                    DELETE FROM libros_por_categoria
                    WHERE categoria=%s
                    AND titulo_libro=%s
                    AND autor_libro= %s
                    """,
                    (row.categoria, titulo_libro, autor_libro)
                )
                session.execute(
                    """
                    INSERT INTO libros_por_categoria
                    (categoria, titulo_libro, autor_libro, calificacion_promedio)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (row.categoria, titulo_libro, autor_libro, calificacion_promedio)
                )
            
            if unica_calificacion:
                session.execute(
                    """
                    DELETE FROM libros_por_categoria
                    WHERE categoria=%s
                    AND titulo_libro=%s
                    AND autor_libro=%s
                    """,
                    (info_previa.categoria, titulo_libro, autor_libro)
                )
    
    else:
        for row in categorias_del_libro:
            session.execute(
                """
                DELETE FROM libros_por_categoria
                WHERE categoria=%s
                AND titulo_libro=%s
                AND autor_libro= %s
                """,
                (row.categoria, titulo_libro, autor_libro)
            )
            session.execute(
                """
                INSERT INTO libros_por_categoria
                (categoria, titulo_libro, autor_libro, calificacion_promedio)
                VALUES (%s, %s, %s, %s)
                """,
                (row.categoria, titulo_libro, autor_libro, calificacion_promedio)
            )

    return 

def Q3_categoría_preferida_por_cliente(id_cliente:str):
    
    resultado = session.execute(
        """
        SELECT categoria, AVG(calificacion) FROM categorias_por_cliente
        WHERE id_cliente=%s
        GROUP BY categoria
        """,
        [id_cliente]
    )

    resultado = pd.DataFrame(resultado.all(), columns=['cateogoria', 'avg_calificacion'])
    resultado = resultado.sort_values(by='avg_calificacion', ascending=False)
    resultado = resultado.values[0]

    return (resultado[0], resultado[1])


def Q4_mas_disfrutaron_libro(titulo_libro:str, autor_libro:str):
    
    resultado_max_calif = session.execute(
        """
        SELECT MAX(calificacion) FROM clientes_por_libro
        WHERE titulo_libro=%s
        AND autor_libro=%s
        LIMIT 1
        """,
        (titulo_libro, autor_libro)
    )

    if resultado_max_calif is None:
        return None

    max_calif = resultado_max_calif.one()[0]

    resultado_clientes = session.execute(
        """
        SELECT id_cliente, calificacion FROM clientes_por_libro
        WHERE titulo_libro=%s
        AND autor_libro=%s
        AND calificacion=%s
        """, 
        (titulo_libro, autor_libro, max_calif)
    )
        
    return pd.DataFrame(resultado_clientes.all())

####################################################################################################################################
#Cargando datos 
print('Cargando datos')
reviews = pd.read_csv('resources/data.csv')
users=pd.read_csv("resources/users.csv")

#Cargamos nuestros datos
for index, row in tqdm(users.iterrows(), total = len(users)):
        Q1_alta_usuario(row[0], row[1], row[2], row[3])

for index, row in tqdm(reviews.iterrows(), total=len(reviews)):
    Q2_agregar_calificacion(row[0], row[1], row[2], row[3], row[4])

#Verificar que los datos fueron cargados 
res = session.execute(
        """
        SELECT * FROM libros_por_cliente
        """
    )
res = pd.DataFrame(res.all())
print(res)