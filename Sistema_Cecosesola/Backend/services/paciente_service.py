from database.db import get_db_connection

class PacienteService:
    @staticmethod
    def obtener_todos():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE activo = 1;")
        pacientes = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return pacientes

    @staticmethod
    def crear_paciente(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO pacientes (cedula_paci, nombre_completo, fecha_naci, sexo, telefono, correo, direccion, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1) RETURNING cedula_paci;
            """, (data.cedula_paci, data.nombre_completo, data.fecha_naci, data.sexo, data.telefono, data.correo, data.direccion))
            cursor.fetchone()
            conn.commit()
            return {"mensaje": "Paciente registrado exitosamente", "cedula": data.cedula_paci}
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def eliminar_paciente(cedula: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE pacientes SET activo = 0 WHERE cedula_paci = ? RETURNING cedula_paci;", (cedula,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return dict(eliminado) if eliminado else None

    @staticmethod
    def actualizar_contacto(cedula: str, datos):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE pacientes 
                SET telefono = ?, correo = ?, direccion = ? 
                WHERE cedula_paci = ? RETURNING cedula_paci;
            """, (datos.telefono, datos.correo, datos.direccion, cedula))
            actualizado = cursor.fetchone()
            conn.commit()
            return dict(actualizado) if actualizado else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()