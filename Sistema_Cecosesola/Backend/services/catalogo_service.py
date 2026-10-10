from database.db import get_db_connection

class CatalogoService:
    @staticmethod
    def obtener_todos():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_servicio, codigo, descripcion, area, precio FROM catalogo_servicio WHERE activo = 1;")
        servicios = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return servicios

    @staticmethod
    def crear_servicio(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO catalogo_servicio (codigo, descripcion, area, precio, activo)
                VALUES (?, ?, ?, ?, 1) RETURNING id_servicio;
            """, (data.codigo, data.descripcion, data.area, data.precio))
            nuevo_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Servicio registrado exitosamente", "id_servicio": nuevo_id}
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def actualizar_servicio(id_servicio: int, data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE catalogo_servicio 
                SET descripcion = COALESCE(?, descripcion),
                    precio = COALESCE(?, precio)
                WHERE id_servicio = ? RETURNING id_servicio;
            """, (data.descripcion, data.precio, id_servicio))
            actualizado = cursor.fetchone()
            conn.commit()
            return dict(actualizado) if actualizado else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def inhabilitar_servicio(id_servicio: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE catalogo_servicio SET activo = 0 WHERE id_servicio = ? RETURNING id_servicio;", (id_servicio,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return dict(eliminado) if eliminado else None