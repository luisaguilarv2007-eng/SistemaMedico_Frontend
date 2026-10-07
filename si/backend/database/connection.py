import sqlite3
import os
from config import settings

def get_db_connection():
    # Retorna una conexión a SQLite usando el archivo configurado
    conn = sqlite3.connect(settings.DB_FILE)
    conn.row_factory = sqlite3.Row
    # Habilitar soporte para llaves foráneas en SQLite
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    # Inicializar la base de datos con DDL si es la primera vez
    conn = get_db_connection()
    # Ejecutamos el script de migraciones/DDL
    with open(os.path.join(os.path.dirname(__file__), "migrations.sql"), "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
