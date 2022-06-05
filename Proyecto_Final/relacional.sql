/*Para borrrar la base de datos*/
DROP DATABASE IF EXISTS panaderia;
CREATE DATABASE  panaderia;
USE panaderia;
/*Sólo en MYSQL podemos usar USE para cambiar de base de datos*/

/*CORTES DE MEDALLAS SEGÚN EL AÑO*/
DROP TABLE IF EXISTS producto;
CREATE TABLE producto(
	id int(3) NOT NULL AUTO_INCREMENT, 
    nombre varchar(30), 
    precio_unit double, 
    descripcion text(500), 
    categoria varchar(30), 
    cantidad_disp int(5), 
    PRIMARY KEY(id)
); 
DROP TABLE IF EXISTS trabajadores;
CREATE TABLE trabajadores(
	curp varchar(20),
    es_admin int(1),  
    nombre varchar(30), 
    apellidos varchar(60), 
    contraseña varchar(10),
    PRIMARY KEY(curp)
); 

DROP TABLE IF EXISTS reporte; 
CREATE TABLE reporte(
	dia date,
    gastos_extras double, 
    ingresos_extras double, 
    ingresos_tienda double, 
    ingresos_vendedores double, 
    ingresos_total double, 
    ganancias_virtual double, 
    ganancias_real double, 
    perdidas_prop double,
    PRIMARY KEY(dia)
); 




