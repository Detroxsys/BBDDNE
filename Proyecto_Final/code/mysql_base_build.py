from datetime import datetime , date
import mysql.connector
import pandas as pd 

mydb = mysql.connector.connect(
  host='localhost',
  port='3306',
  user='root',
  password='password'
)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS panaderia")
mycursor.execute("CREATE DATABASE  panaderia")

mycursor.execute("SHOW DATABASES")

#for x in mycursor:
#  print(x)


mydb = mysql.connector.connect(
  host='localhost',
  port='3306',
  user='root',
  password='password',
  database="panaderia"
)

mycursor = mydb.cursor()

mycursor.execute("""
                    CREATE TABLE productos(
                        id int(3) NOT NULL AUTO_INCREMENT, 
                        nombre varchar(30), 
                        precio_unit double, 
                        descripcion text(500), 
                        categoria varchar(30), 
                        cantidad_disp int, 
                        PRIMARY KEY(id)
                    )
                """)

mycursor.execute("""
                    CREATE TABLE trabajadores(
                        RFC varchar(20) NOT NULL,
                        es_admin int(1) DEFAULT 0,  
                        nombre varchar(30), 
                        apellidos varchar(60), 
                        contraseña varchar(50),
                        PRIMARY KEY(RFC)
                    )
                """)


mycursor.execute("""
                    CREATE TABLE hist_gastos(
                        fecha datetime, 
                        concepto text(500),
                        costo    double, 
                        usuario  varchar(20) NOT NULL,
                        FOREIGN KEY(usuario) REFERENCES trabajadores(RFC) ON DELETE CASCADE,
                        PRIMARY KEY(fecha)
                    )
                """)

mycursor.execute("""
                    CREATE TABLE hist_ingresos_extras(
                        fecha datetime, 
                        concepto text(500),
                        ingreso    double, 
                        usuario  varchar(20) NOT NULL,
                        FOREIGN KEY(usuario) REFERENCES trabajadores(RFC) ON DELETE CASCADE,
                        PRIMARY KEY(fecha)
                    )
                """)


mycursor.execute("""
                    CREATE TABLE reportes(
                        dia date,
                        gastos_extras double, 
                        ingresos_extras double, 
                        ingresos_tienda double, 
                        ingresos_total double, 
                        ganancias_virtual double, 
                        ganancias_real double, 
                        perdidas_prop double,
                        PRIMARY KEY(dia)
                    )
                """)

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)


def nuevo_producto(nombre: str, precio_unit: float, descripcion: str, categoria: str, cantidad_disp: int):    
    sql = "INSERT INTO productos (nombre, precio_unit, descripcion, categoria, cantidad_disp) VALUES (%s, %s, %s, %s, %s)"
    val = [nombre, precio_unit, descripcion, categoria, cantidad_disp]
    mycursor.execute(sql, val)
    mydb.commit()
    return 


def nuevo_usuario( rfc: str, es_admin: int, nombre: str, apellidos: str, contraseña: str):
    sql = "INSERT INTO trabajadores (rfc, es_admin, nombre, apellidos, contraseña) VALUES (%s, %s, %s, %s, %s)"
    val = [rfc, es_admin, nombre, apellidos, contraseña]
    mycursor.execute(sql, val)
    mydb.commit()
    return 

nuevo_usuario("LAMY0004069N5", 1, "Yeudiel", "Lara Moreno", "12345")
df_productos = pd.read_csv('data\productos.csv')
#Cargamos nuestros datos
for index, row in df_productos.iterrows():
        nuevo_producto(row[0], row[1], row[2], row[3], row[4])




