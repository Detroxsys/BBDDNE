# Proyecto Final de la materia

## Bibliotecas:
**Drivers para bases de datos**
* `pip install pymongo`
* `pip install redis`
* `pip install mysql-connector-python`

**Interfaz**
* `pip install tkinter`

**Otros**
* `pip install pandas`

## CARACTERÍSTICAS DEL PROGRAMA:
Aplicación que lleva la contabilidad de la panadería *El Volován*.

## Prerequisitos:
1. Crear contenedor con MySql: `docker run --name user_mysql_1 --env="MYSQL_ROOT_PASSWORD=password" -p 3306:3306 -d mysql:latest`
2. Crear contenedor con MongoDB: `docker run --name my-mongo -p 27017:27017 -d mongo ` 
3. Crear contenedor con Redis: `docker run --name my-redis -p 6379:6379 -d redis ` 


## INSTRUCCIONES DE USO:
1. Realizar los prerequisitos.
2. Ejecutar los contenedores creados.

## ADVERTENCIAS:
- Para que los directorios funcionen se debe abrir la carpeta entera (PROYECTO_FINAL) desde VSCode, de otro modo se tendran que indicar la ruta específica de cada archivo.
- Si al desplegar una ventana en una consulta, esta sale en blanco, significa que no existen registros para dicha consulta.
