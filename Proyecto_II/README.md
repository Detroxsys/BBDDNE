# Proyecto II

Recursos:
 - https://docs.datastax.com/en/developer/python-driver/3.25/getting_started/
 - https://cassandra.apache.org/doc/latest/cassandra/faq/
 - https://openwebinars.net/blog/como-usar-apache-cassandra-con-python/
 - https://docs.datastax.com/en/cql-oss/3.3/cql/cql_reference/cqlCreateTable.html
 - https://www.datastax.com/blog/most-important-thing-know-cassandra-data-modeling-primary-key

Bibliotecas:
%pip install cassandra-driver
%pip install tk
%pip install pillow
%pip install pandastable
%pip install tqdm
%pip install pandas

CARACTERÍSTICAS DEL PROGRAMA:
- Los usuarios ingresan con nombre de usuario
- Existe un sólo usuario de administrador llamado admin

INSTRUCCIONES DE USO:
1- Installar bibliotecas requeridas
2- Crear un contenedor de Cassandra usando Docker, es importante mapear al puerto 9042 durante la creación
3- Ejecutar base_queries.py, esto cargará los datos reunidos a la base en Cassandra y compilará las querys utilizadas en la UI
4- Ejecutar login.py

ADVERTENCIAS:
- Para que los directorios funcionen se debe abrir la carpeta entera (PROYECTO II) desde VSCode, de otro modo se tendran que indicar la ruta específica de cada archivo.