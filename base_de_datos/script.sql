CREATE DATABASE clinica_db;
\c clinica_db

CREATE TABLE pacientes (
    id             SERIAL PRIMARY KEY,
    cedula         VARCHAR(10)  UNIQUE NOT NULL,
    nombre         VARCHAR(100) NOT NULL,
    apellido       VARCHAR(100) NOT NULL,
    edad           INTEGER      NOT NULL,
    telefono       VARCHAR(15)  NOT NULL,
    email          VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);