# Proyecto 4: Neo4j

## Recursos
- [Documentación NeoModel](https://neomodel.readthedocs.io/en/latest/index.html)

## Bibliotecas
- %pip install neo4j
- %pip install neomodel
- %pip install pillow
- %pip install pandastable
- %pip install pandas

## CARACTERÍSTICAS DEL PROGRAMA:
Aplicación de viajes en bicicleta que permite a los usuarios tener lugares preferidos guardados y conocer las estaciones de bicicleta más cercanas a estos lugares.
También es posible planear rutas a partir de un lugar o estación seleccionada y un tiempo deseado.
- Los usuarios ingresan con nombre de usuario y deben añadir un lugar (ej. Casa, Trabajo) junto con su ubicación.
- Los usuarios pueden realizar alguna de las siguientes acciones:
  - Consultar tiendas en un estado que tienen un producto.
  - Verificar si una tienda de algun estado tiene algun incumplimiento. 
  - Buscar una tienda sin incumplimientos para un estado y producto dado. 
  - Registro de compras y lugares de un usuario. 
  - Organizar estados por el ratio del cumplimiento de sus tiendas.
  - Recibir recomendaciones según lo que otros usuarios han comprado. 

## INSTRUCCIONES DE USO:
1. Instalar bibliotecas requeridas.
2. Crear un contenedor de Neo4j utilizando Docker,es importante mapear al puerto 7687 y 7474 durante la creación de este.
3. Ejecutar el contenedor.
4. clean_data.ipynb se utiliza para limpiar los datos y obtener el archivo Tiendas_limpio.csv para cargar los datos. 
5. Ejecutar base_construction.py, esto creará la base en el servidor y cargará los datos reunidos a la base.
6. Ejecutar login.py, esto desplegará una ventana con la interfaz gráfica de la aplicación. No hay usuarios precargados.

## ADVERTENCIAS:
- Para que los directorios funcionen se debe abrir la carpeta entera (PROYECTO_IV) desde VSCode, de otro modo se tendran que indicar la ruta específica de cada archivo.
- Si al desplegar una ventana en una consulta, esta sale en blanco, significa que no existen registros para dicha consulta.
