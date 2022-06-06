from datetime import datetime , date
import mysql.connector
import pandas as pd 

mydb = mysql.connector.connect(
  host='localhost',
  port='3306',
  user='root',
  password='password',
  database="panaderia"
)

mycursor = mydb.cursor()


def existe_producto(nombre : str): 
    mycursor.execute(
        """
            SELECT * FROM productos
            WHERE nombre = %s
            LIMIT 1
        """, 
        [nombre]
    )
    myresult = mycursor.fetchone()

    if myresult: 
        return True 
    return False

def nuevo_producto(nombre: str, precio_unit: float, descripcion: str, categoria: str, cantidad_disp: int):    
    sql = "INSERT INTO productos (nombre, precio_unit, descripcion, categoria, cantidad_disp) VALUES (%s, %s, %s, %s, %s)"
    val = [nombre, precio_unit, descripcion, categoria, cantidad_disp]
    mycursor.execute(sql, val)
    mydb.commit()
    return 


def update_cant_producto(nombre: str, cantidad_disp: int): 
    sql = "UPDATE productos SET cantidad_disp = %s WHERE nombre = %s"
    val = [cantidad_disp, nombre]
    mycursor.execute(sql, val)
    mydb.commit()
    return


def get_all_productos(): 
    result = pd.read_sql("SELECT nombre, precio_unit, cantidad_disp FROM productos", mydb)
    return result


def existe_usuario( rfc: str):
    mycursor.execute(
        """
            SELECT * FROM trabajadores
            WHERE rfc = %s
            LIMIT 1
        """, 
        [rfc]
    )
    myresult = mycursor.fetchone()

    if myresult: 
        return True 
    return False 

def is_admin ( rfc: str): 
    mycursor.execute(
        """
            SELECT es_admin FROM trabajadores
            WHERE rfc = %s
            LIMIT 1
        """, 
        [rfc]
    )
    myresult = mycursor.fetchone()      
    if myresult[0]==1: 
        return True 
    return False 

def get_password( rfc: str): 
    mycursor.execute(
        """
            SELECT contraseña FROM trabajadores
            WHERE rfc = %s
            LIMIT 1
        """, 
        [rfc]
    )
    myresult = mycursor.fetchone() 
    return myresult[0]

def nuevo_usuario( rfc: str, es_admin: int, nombre: str, apellidos: str, contraseña: str):
    sql = "INSERT INTO trabajadores (rfc, es_admin, nombre, apellidos, contraseña) VALUES (%s, %s, %s, %s, %s)"
    val = [rfc, es_admin, nombre, apellidos, contraseña]
    mycursor.execute(sql, val)
    mydb.commit()
    return 


def guardar_gasto(fecha: datetime, concepto: str, costo: float, usuario: str): 
    sql = "INSERT INTO hist_gastos (fecha, concepto, costo, usuario) VALUES (%s, %s, %s, %s)"
    val = [fecha, concepto, costo, usuario]
    mycursor.execute(sql, val)
    mydb.commit()
    return 


def guardar_ingreso(fecha: datetime, concepto: str, ingreso: float, usuario: str): 
    sql = "INSERT INTO hist_ingresos_extras (fecha, concepto, ingreso, usuario) VALUES (%s, %s, %s, %s)"
    val = [fecha, concepto, ingreso, usuario]
    mycursor.execute(sql, val)
    mydb.commit()
    return

def guardar_reporte(dia: date, gastos_extras: float, 
                    ingresos_extras: float, ingresos_tienda: float, ingresos_total: float, 
                    ganancias_virtual: float, ganancias_real: float, perdidas_prop: float):
    sql = """
            INSERT INTO reportes VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
          """
    val = [dia, gastos_extras, ingresos_extras, ingresos_tienda, ingresos_total, 
           ganancias_virtual, ganancias_real, perdidas_prop]
    mycursor.execute(sql, val)
    mydb.commit()
    return  


#print(get_all_productos())