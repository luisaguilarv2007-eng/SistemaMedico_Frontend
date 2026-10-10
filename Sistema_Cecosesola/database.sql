--create database SantaCruz_Sistema;

-- =================================================================
-- SCRIPT DE BASE DE DATOS: INFOLAB - CECOCESOLA SANTA CRUZ
-- MOTOR: PostgreSQL
-- =================================================================

-- 1. Tabla Usuarios (Seguridad y Personal)
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    rol VARCHAR(10) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- 2. Tabla Pacientes (Ficha Única)
CREATE TABLE pacientes (
    cedula_paci VARCHAR(20) PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    fecha_naci DATE,
    sexo CHAR(1),
    telefono VARCHAR(20),
    correo VARCHAR(200),
    direccion VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);

-- 3. Tabla Catálogo de Servicios
CREATE TABLE catalogo_servicio (
    id_servicio SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE,
    descripcion VARCHAR(255) NOT NULL,
    area VARCHAR(50) NOT NULL,
    precio NUMERIC(12, 2) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- 4. Tabla Órdenes (Maestro del flujo clínico)
CREATE TABLE ordenes (
    id_orden SERIAL PRIMARY KEY,
    cedula_paci VARCHAR(20) REFERENCES pacientes(cedula_paci),
    id_medico_tratante INTEGER REFERENCES usuarios(id_usuario),
    fecha_creacion TIMESTAMP(0) WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'En Espera',
    autorizado BOOLEAN DEFAULT FALSE
);

-- 5. Tabla Detalles de Orden (Estudios asignados)
CREATE TABLE orden_detalles (
    id_detalle BIGSERIAL PRIMARY KEY,
    id_orden INTEGER REFERENCES ordenes(id_orden) ON DELETE CASCADE,
    id_servicio INTEGER REFERENCES catalogo_servicio(id_servicio),
    estado_examen VARCHAR(30) DEFAULT 'Pendiente',
    id_usuario_procesa INTEGER REFERENCES usuarios(id_usuario),
    id_usuario_valida INTEGER REFERENCES usuarios(id_usuario),
    datos_laboratorio JSONB,
    informe_radiologico TEXT
);

-- 6. Tabla Documentos de Facturación
CREATE TABLE documentos_facturacion (
    id_documento SERIAL PRIMARY KEY,
    id_orden INTEGER REFERENCES ordenes(id_orden),
    cedula_paci VARCHAR(20) REFERENCES pacientes(cedula_paci),
    tipo_documento VARCHAR(20) NOT NULL,
    razon_social VARCHAR(150),
    fecha_emision TIMESTAMP(0) WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    subtotal NUMERIC(12, 2) NOT NULL,
    iva NUMERIC(12, 2) NOT NULL,
    monto_total NUMERIC(12, 2) NOT NULL,
    estado_pago VARCHAR(20) DEFAULT 'Pendiente',
    id_cajero INTEGER REFERENCES usuarios(id_usuario)
);

-- 7. Tabla Pagos Recibidos
CREATE TABLE pagos_recibidos (
    id_pago SERIAL PRIMARY KEY,
    id_documento INTEGER REFERENCES documentos_facturacion(id_documento) ON DELETE CASCADE,
    metodo_pago INTEGER NOT NULL,
    monto_pagado NUMERIC(12, 2) NOT NULL,
    referencia VARCHAR(50),
    fecha_pago TIMESTAMP(0) WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Tabla Archivos Adjuntos (PDFs)
CREATE TABLE archivos_adjuntos (
    id_archivo BIGSERIAL PRIMARY KEY,
    id_detalle BIGINT REFERENCES orden_detalles(id_detalle) ON DELETE CASCADE,
    url_archivo TEXT NOT NULL,
    tipo_archivo VARCHAR(50)
);

-- 9. Tabla Envíos Automatizados (WhatsApp/Correo)
CREATE TABLE envios_automatizados (
    id_envio BIGSERIAL PRIMARY KEY,
    id_orden INTEGER REFERENCES ordenes(id_orden) ON DELETE CASCADE,
    canal VARCHAR(20) NOT NULL,
    fecha_envio TIMESTAMP(0) WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    estado_enviado BOOLEAN DEFAULT FALSE,
    msj_error TEXT
);

-- 10. Tabla Bitácora de Auditoría
CREATE TABLE bitacora_auditoria (
    id_log BIGSERIAL PRIMARY KEY,
    fecha_hora TIMESTAMP(0) WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuarios(id_usuario),
    modulo_afectado VARCHAR(100) NOT NULL,
    detalle_cambio JSONB NOT NULL
);

select * from pacientes where activo=false;

ALTER TABLE usuarios ALTER COLUMN rol TYPE VARCHAR(50);

select * from pagos_recibidos
