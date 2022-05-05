# Proyecto III

## Recursos
- [Documentación PyMongo](https://pymongo.readthedocs.io/en/stable/tutorial.html)
- [Documentación Mongo](https://www.mongodb.com/docs/)

## Bibliotecas
- %pip install pymongo
- %pip install tk
- %pip install pillow
- %pip install pandastable
- %pip install pandas

## CARACTERÍSTICAS DEL PROGRAMA:
Aplicación de viajes en bicicleta que permite a los usuarios tener lugares preferidos guardados y conocer las estaciones de bicicleta más cercanas a estos lugares.
También es posible planear rutas a partir de un lugar o estación seleccionada y un tiempo deseado.
- Los usuarios ingresan con nombre de usuario y deben añadir un lugar (ej. Casa, Trabajo) junto con su ubicación.
- Los usuarios pueden realizar alguna de las siguientes acciones:
  - Añadir un nuevo lugar guardado o actualizar uno existente.
  - Consultar sus lugares guardados.
  - Consultar las estaciones más cercanas a los lugares guardados.
  - Planear viajes, seleccionando alguna de sus estaciones cercanas o una estación preferida.
  - Consultar el historial de viajes realizados.    

## INSTRUCCIONES DE USO:
1. Instalar bibliotecas requeridas.
2. Crear un contenedor de Mongo usando Docker, es importante mapear al puerto 27017 durante la creación de este.
3. Ejecutar el contenedor.
4. Ejecutar base_construction.py, esto creará la base `BDBicis` en el servidor y cargará los datos reunidos a la base.
6. Ejecutar login.py, esto desplegará una ventana con la interfaz gráfica de la aplicación.
7. Se puede crear un nuevo usuario o usar el siguiente usuario precargado : `ProfePime`.

## ADVERTENCIAS:
- Para que los directorios funcionen se debe abrir la carpeta entera (PROYECTO_III) desde VSCode, de otro modo se tendran que indicar la ruta específica de cada archivo.
- Si al desplegar una ventana en una consulta, esta sale en blanco, significa que no existen registros para dicha consulta.
- Para un tiempo de viaje seleccionado y una estación elegida, es posible que no se muestren sugerencias en "estación final", esto se debe a que se muestran únicamente resultados dentro de un rango de +-60 minutos del tiempo elegido.
