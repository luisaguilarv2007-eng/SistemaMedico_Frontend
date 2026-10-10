import os
import sqlite3
import hashlib
from pathlib import Path

# Ruta persistente de la base de datos SQLite
DB_PATH = Path(__file__).resolve().parent.parent / "santacruz_sistema.db"

def get_db_connection():
    """
    Retorna una conexión a SQLite configurada con row_factory para soporte de diccionarios
    y activación de Foreign Keys.
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """
    Crea las tablas automáticamente e inserta datos iniciales de prueba si la base de datos está vacía.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Tabla Usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            password VARCHAR(255) NOT NULL,
            nombre VARCHAR(255) NOT NULL,
            rol VARCHAR(50) NOT NULL,
            activo BOOLEAN DEFAULT 1
        );
    """)

    # 2. Tabla Pacientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            cedula_paci VARCHAR(20) PRIMARY KEY,
            nombre_completo VARCHAR(100) NOT NULL,
            fecha_naci DATE,
            sexo CHAR(1),
            telefono VARCHAR(20),
            correo VARCHAR(200),
            direccion VARCHAR(255),
            activo BOOLEAN DEFAULT 1
        );
    """)

    # 3. Tabla Catálogo de Servicios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS catalogo_servicio (
            id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo VARCHAR(50) UNIQUE,
            descripcion VARCHAR(255) NOT NULL,
            area VARCHAR(50) NOT NULL,
            precio NUMERIC(12, 2) NOT NULL,
            activo BOOLEAN DEFAULT 1
        );
    """)

    # 4. Tabla Órdenes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordenes (
            id_orden INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula_paci VARCHAR(20) REFERENCES pacientes(cedula_paci),
            id_medico_tratante INTEGER REFERENCES usuarios(id_usuario),
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            estado VARCHAR(20) DEFAULT 'En Espera',
            autorizado BOOLEAN DEFAULT 0
        );
    """)

    # 5. Tabla Detalles de Orden
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orden_detalles (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_orden INTEGER REFERENCES ordenes(id_orden) ON DELETE CASCADE,
            id_servicio INTEGER REFERENCES catalogo_servicio(id_servicio),
            estado_examen VARCHAR(30) DEFAULT 'Pendiente',
            id_usuario_procesa INTEGER REFERENCES usuarios(id_usuario),
            id_usuario_valida INTEGER REFERENCES usuarios(id_usuario),
            datos_laboratorio TEXT,
            informe_radiologico TEXT
        );
    """)

    # 6. Tabla Documentos de Facturación
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos_facturacion (
            id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_orden INTEGER REFERENCES ordenes(id_orden),
            cedula_paci VARCHAR(20) REFERENCES pacientes(cedula_paci),
            tipo_documento VARCHAR(20) NOT NULL,
            razon_social VARCHAR(150),
            fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
            subtotal NUMERIC(12, 2) NOT NULL,
            iva NUMERIC(12, 2) NOT NULL,
            monto_total NUMERIC(12, 2) NOT NULL,
            estado_pago VARCHAR(20) DEFAULT 'Pendiente',
            id_cajero INTEGER REFERENCES usuarios(id_usuario)
        );
    """)

    # 7. Tabla Pagos Recibidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagos_recibidos (
            id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
            id_documento INTEGER REFERENCES documentos_facturacion(id_documento) ON DELETE CASCADE,
            metodo_pago INTEGER NOT NULL,
            monto_pagado NUMERIC(12, 2) NOT NULL,
            referencia VARCHAR(50),
            fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 8. Tabla Archivos Adjuntos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS archivos_adjuntos (
            id_archivo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_detalle INTEGER REFERENCES orden_detalles(id_detalle) ON DELETE CASCADE,
            url_archivo TEXT NOT NULL,
            tipo_archivo VARCHAR(50)
        );
    """)

    # 9. Tabla Envíos Automatizados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS envios_automatizados (
            id_envio INTEGER PRIMARY KEY AUTOINCREMENT,
            id_orden INTEGER REFERENCES ordenes(id_orden) ON DELETE CASCADE,
            canal VARCHAR(20) NOT NULL,
            fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
            estado_enviado BOOLEAN DEFAULT 0,
            msj_error TEXT
        );
    """)

    # 10. Tabla Bitácora de Auditoría
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bitacora_auditoria (
            id_log INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            id_usuario INTEGER REFERENCES usuarios(id_usuario),
            modulo_afectado VARCHAR(100) NOT NULL,
            detalle_cambio TEXT NOT NULL
        );
    """)

    conn.commit()

    # --- SEED DE DATOS INICIALES (si las tablas están vacías) ---
    cursor.execute("SELECT COUNT(*) FROM usuarios;")
    if cursor.fetchone()[0] == 0:
        def hash_pass(p):
            return hashlib.sha256(p.encode('utf-8')).hexdigest()

        # Usuarios iniciales
        cursor.execute("INSERT INTO usuarios (nombre, password, rol, activo) VALUES (?, ?, ?, 1);",
                       ("admin", hash_pass("admin123"), "Administrador"))
        cursor.execute("INSERT INTO usuarios (nombre, password, rol, activo) VALUES (?, ?, ?, 1);",
                       ("Dra. Maria Perez", hash_pass("medico123"), "Médico"))
        cursor.execute("INSERT INTO usuarios (nombre, password, rol, activo) VALUES (?, ?, ?, 1);",
                       ("Lic. Carlos Soto", hash_pass("lab123"), "Laboratorio"))
        cursor.execute("INSERT INTO usuarios (nombre, password, rol, activo) VALUES (?, ?, ?, 1);",
                       ("Ana Gomez", hash_pass("caja123"), "Caja"))

        # Pacientes iniciales
        cursor.execute("""
            INSERT INTO pacientes (cedula_paci, nombre_completo, fecha_naci, sexo, telefono, correo, direccion, activo)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1);
        """, ("V-12345678", "Juan Perez", "1988-04-12", "M", "0414-5551234", "juan.perez@email.com", "Barquisimeto, Lara"))
        cursor.execute("""
            INSERT INTO pacientes (cedula_paci, nombre_completo, fecha_naci, sexo, telefono, correo, direccion, activo)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1);
        """, ("V-23456789", "Maria Garcia", "1994-09-23", "F", "0424-7778899", "maria.garcia@email.com", "Cabudare, Palavecino"))

        # Catálogo de servicios inicial
        servicios_iniciales = [
            ("LAB-001", "Hematología Completa", "Laboratorio", 12.00),
            ("LAB-002", "Perfil Lipídico (Colesterol + Triglicéridos)", "Laboratorio", 18.00),
            ("LAB-003", "Glicemia en Ayunas", "Laboratorio", 8.00),
            ("LAB-004", "Examen de Orina / Uroanálisis", "Laboratorio", 7.00),
            ("RX-001", "Radiografía de Tórax PA", "Rayos X", 25.00),
            ("ECO-001", "Ecografía Abdominal Completa", "Ecografía", 35.00),
            ("ODO-001", "Limpieza Dental y Diagnóstico", "Odontología", 20.00),
        ]
        for codigo, desc, area, precio in servicios_iniciales:
            cursor.execute("""
                INSERT INTO catalogo_servicio (codigo, descripcion, area, precio, activo)
                VALUES (?, ?, ?, ?, 1);
            """, (codigo, desc, area, precio))

        conn.commit()

    conn.close()

# Inicializar esquema al importar
init_db()