/*Para borrrar la base de datos*/
DROP DATABASE IF EXISTS panaderia;
CREATE DATABASE  panaderia;
USE panaderia;
/*Sólo en MYSQL podemos usar USE para cambiar de base de datos*/

/*CORTES DE MEDALLAS SEGÚN EL AÑO*/
DROP TABLE IF EXISTS productos;
CREATE TABLE productos(
                        id int(3) NOT NULL AUTO_INCREMENT, 
                        nombre varchar(30), 
                        precio_unit double, 
                        descripcion text(500), 
                        categoria varchar(30), 
                        cantidad_disp int, 
                        PRIMARY KEY(id)
                    ); 
DROP TABLE IF EXISTS trabajadores;
CREATE TABLE trabajadores(
                        RFC varchar(20) NOT NULL,
                        es_admin int(1) DEFAULT 0,  
                        nombre varchar(30), 
                        apellidos varchar(60), 
                        contraseña varchar(50),
                        PRIMARY KEY(RFC)
                    ); 

DROP TABLE IF EXISTS hist_gastos; 
CREATE TABLE hist_gastos(
	fecha datetime, 
    concepto text(500),
    costo    double, 
    usuario  varchar(20) NOT NULL,
    FOREIGN KEY(usuario) REFERENCES trabajadores(RFC) ON DELETE CASCADE,
    PRIMARY KEY(fecha)
);

DROP TABLE IF EXISTS hist_ingresos_extras; 
CREATE TABLE hist_ingresos_extras(
	fecha datetime, 
    concepto text(500),
    ingreso    double, 
    usuario  varchar(20) NOT NULL,
    FOREIGN KEY(usuario) REFERENCES trabajadores(RFC) ON DELETE CASCADE,
    PRIMARY KEY(fecha)
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




