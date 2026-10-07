import sqlite3
from typing import List, Optional
from models.producto import ProductoCreate, ProductoUpdate
from database.connection import get_db_connection

class ProductoService:
    # Capa de Servicios: Contiene las reglas de negocio y acceso a base de datos
    
    @staticmethod
    def get_all_active_productos():
        """Obtiene todos los productos activos."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE estado = 1")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_producto_by_id(producto_id: int):
        """Obtiene un producto específico que esté activo."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ? AND estado = 1", (producto_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def create_producto(data: ProductoCreate):
        """Crea un nuevo producto tras validar reglas de negocio."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Regla de negocio: Validar que la categoría exista
            cursor.execute("SELECT id FROM categorias WHERE id = ?", (data.categoria_id,))
            if not cursor.fetchone():
                raise ValueError("La categoría especificada no existe.")
            
            cursor.execute("""
                INSERT INTO productos (nombre, descripcion, categoria_id, precio, stock)
                VALUES (?, ?, ?, ?, ?)
            """, (data.nombre, data.descripcion, data.categoria_id, data.precio, data.stock))
            conn.commit()
            producto_id = cursor.lastrowid
            return ProductoService.get_producto_by_id(producto_id)
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise ValueError(f"Error de integridad en base de datos: el nombre ya existe u otro error ({str(e)}).")
        finally:
            conn.close()

    @staticmethod
    def update_producto(producto_id: int, data: ProductoUpdate):
        """Actualiza la información de un producto."""
        producto_actual = ProductoService.get_producto_by_id(producto_id)
        if not producto_actual:
            return None
        
        # Filtramos campos que no fueron proveídos en la solicitud
        updates = []
        params = []
        for key, value in data.model_dump(exclude_unset=True).items():
            updates.append(f"{key} = ?")
            params.append(value)
            
        if not updates:
            return producto_actual

        updates.append("fecha_actualizacion = CURRENT_TIMESTAMP")
        query = f"UPDATE productos SET {', '.join(updates)} WHERE id = ? AND estado = 1"
        params.append(producto_id)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if 'categoria_id' in data.model_dump(exclude_unset=True):
                cursor.execute("SELECT id FROM categorias WHERE id = ?", (data.categoria_id,))
                if not cursor.fetchone():
                    raise ValueError("La categoría especificada no existe.")

            cursor.execute(query, tuple(params))
            conn.commit()
            return ProductoService.get_producto_by_id(producto_id)
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise ValueError(f"Error de integridad en base de datos: el nombre ya existe u otro error ({str(e)}).")
        finally:
            conn.close()

    @staticmethod
    def soft_delete_producto(producto_id: int):
        """Borrado lógico (estado = false)."""
        producto_actual = ProductoService.get_producto_by_id(producto_id)
        if not producto_actual:
            return False
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET estado = 0, fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = ?", (producto_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all_categorias():
        """Lista todas las categorías."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categorias")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def create_categoria(nombre: str):
        """Crea una nueva categoría."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
            conn.commit()
            cat_id = cursor.lastrowid
            cursor.execute("SELECT * FROM categorias WHERE id = ?", (cat_id,))
            row = cursor.fetchone()
            return dict(row)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError("La categoría ya existe.")
        finally:
            conn.close()
