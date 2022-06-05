Integrantes: 
Marcela Cruz Larios 
Yeudiel Lara Moreno
Pablo David Castillo del Valle


Para que funcione el programa deben instalarse las siguientes bibliotecas: 
bcrypt
pyshorteners

El archivo ejecutable es FrontEnd.py
Los archivos .py deben estar en el mismo directorio para el correcto funcionamiento del programa. 

Por defecto el administrador es ADMIN con contraseña 123.

Es necesario que exista un contenedor con una instancia de redis
y con las siguientes especificaciones: 
redis.Redis(host='127.0.0.1', port=6379, db=0)
-p 6379:6379
 
El programa corre en cache mientras este activo pero cada que se cierra el programa
se guarda en memoria para no perder la información. 



