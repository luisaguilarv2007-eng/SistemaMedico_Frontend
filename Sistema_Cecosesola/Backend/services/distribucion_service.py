from database.db import get_db_connection

class DistribucionService:
    # --- Lógica de Archivos Adjuntos ---
    @staticmethod
    def guardar_adjunto(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO archivos_adjuntos (id_detalle, url_archivo, tipo_archivo)
                VALUES (?, ?, ?) RETURNING id_archivo;
            """, (data.id_detalle, data.url_archivo, data.tipo_archivo))
            nuevo_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Archivo PDF adjuntado correctamente", "id_archivo": nuevo_id}
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def eliminar_adjunto(id_archivo: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM archivos_adjuntos WHERE id_archivo = ? RETURNING id_archivo;", (id_archivo,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return dict(eliminado) if eliminado else None

    # --- Lógica de Envíos (WhatsApp/Correo) ---
    @staticmethod
    def programar_envio(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO envios_automatizados (id_orden, canal, estado_enviado)
                VALUES (?, ?, 0) RETURNING id_envio;
            """, (data.id_orden, data.canal))
            nuevo_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": f"Envío programado vía {data.canal}", "id_envio": nuevo_id}
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def actualizar_estado_envio(id_envio: int, data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE envios_automatizados
                SET estado_enviado = ?, msj_error = ?
                WHERE id_envio = ? RETURNING id_envio;
            """, (1 if data.estado_enviado else 0, data.msj_error, id_envio))
            actualizado = cursor.fetchone()
            conn.commit()
            return dict(actualizado) if actualizado else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def obtener_archivos():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_archivo, id_detalle, url_archivo FROM archivos_adjuntos;")
        archivos = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return archivos

    @staticmethod
    def obtener_envios():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_envio, id_orden, canal, estado_enviado, msj_error FROM envios_automatizados;")
        envios = []
        for r in cursor.fetchall():
            d = dict(r)
            d['estado_enviado'] = bool(d.get('estado_enviado'))
            envios.append(d)
        conn.close()
        return envios