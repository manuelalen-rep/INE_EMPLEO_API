CREATE DATABASE STAGING;

CREATE TABLE STAGING.COMPOSICION_SALARIO_BRUTO(
sexo varchar(90),
cno11 varchar(90),
componentes_salario varchar(90),
salario float
);

CREATE TABLE STAGING.OCUPACIONES(
ocupacion varchar(90),
sexo varchar(90),
tipo_dato varchar(90),
periodo int,
numero_trabajadores float
);


-- BRONZE

CREATE DATABASE BRONZE;
CREATE TABLE BRONZE.OCUPACIONES(
ocupacion longtext,
sexo longtext,
tipo_dato longtext,
periodo int,
numero_trabajadores float);

CREATE TABLE BRONZE.COMPOSICION_SALARIO_BRUTO(
sexo varchar(90),
cno11 longtext,
componentes_salario longtext,
salario float
);

--SILVER
CREATE DATABASE SILVER;
CREATE TABLE SILVER.OCUPACIONES_ABSOLUTOS(
ocupacion longtext,
sexo longtext,
tipo_dato longtext,
periodo int,
numero_trabajadores float
);

CREATE TABLE SILVER.COMPOSICION_SALARIO_BRUTO(
sexo varchar(90),
cno11 longtext,
componentes_salario longtext,
salario float
);