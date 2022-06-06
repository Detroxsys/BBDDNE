# Proyecto Final de la materia

## Descripción del programa:
Aplicación que lleva la contabilidad de la panadería *El Volován*.

## Bibliotecas requeridas:
**Drivers para bases de datos**
* `pip install pymongo`
* `pip install redis`
* `pip install mysql-connector-python`

**Interfaz**
* `pip install tk`
* `pip install pillow`
* `pip install tkcalendar`

**Otros**
* `pip install pandas`

## Prerequisitos:
1. Instalar Python y bibliotecas requeridas.
1. Crear contenedor con MySql: `docker run --name user_mysql_1 --env="MYSQL_ROOT_PASSWORD=password" -p 3306:3306 -d mysql:latest`
2. Crear contenedor con MongoDB: `docker run --name my-mongo -p 27017:27017 -d mongo ` 
3. Crear contenedor con Redis: `docker run --name my-redis -p 6379:6379 -d redis ` 


## INSTRUCCIONES DE USO:
1. Completar los prerequisitos
2. Ejecutar los contenedores creados para las bases.
3. Abrir el proyecto directo desde la carpeta `PROYECTO_FINAL`.
4. Ejecutar archivo `code/mysql_base_build.py`. Este construye la base de datos en MySQL.
4. Ejecutar archivo `code/mongo_base_build.py`. Este construye la base de datos en MongoDB.
5. Ejecutar archivo `code/redis_base_build.py`. Este construye la base de datos en Redis.
6. Ejecutar archivo `code/gui.py`. Este abre la interfaz gráfica de la aplicación en una ventana.
7. Se puede crear un nuevo usuario o ingresar con las credenciales de administrador (*RFC:* **LAMY0004069N5**, *contraseña:* **12345**).

## ADVERTENCIAS:
- Para que los directorios funcionen se debe abrir la carpeta entera (PROYECTO_FINAL) desde VSCode, de otro modo se tendran que indicar la ruta específica de cada archivo.
- Si al desplegar una ventana en una consulta, esta sale en blanco, significa que no existen registros para dicha consulta.
