import hashlib
from database.db import get_db_connection

class UsuarioService:
    @staticmethod
    def encriptar_password(password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def obtener_todos():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, rol FROM usuarios WHERE activo = 1;")
        usuarios = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return usuarios

    @staticmethod
    def crear_usuario(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            pass_encriptada = UsuarioService.encriptar_password(data.password)
            cursor.execute("""
                INSERT INTO usuarios (nombre, password, rol, activo)
                VALUES (?, ?, ?, 1) RETURNING id_usuario;
            """, (data.nombre, pass_encriptada, data.rol))
            nuevo_id = cursor.fetchone()[0]
            conn.commit()
            return {"mensaje": "Usuario creado y contraseña encriptada exitosamente", "id_usuario": nuevo_id}
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def validar_login(usuario: str, password_plana: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        pass_encriptada = UsuarioService.encriptar_password(password_plana)
        cursor.execute("""
            SELECT id_usuario, nombre, rol FROM usuarios 
            WHERE nombre = ? AND password = ? AND activo = 1;
        """, (usuario, pass_encriptada))
        usuario_valido = cursor.fetchone()
        conn.close()
        return dict(usuario_valido) if usuario_valido else None

    @staticmethod
    def inhabilitar_usuario(id_usuario: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET activo = 0 WHERE id_usuario = ? RETURNING id_usuario;", (id_usuario,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return dict(eliminado) if eliminado else None

    @staticmethod
    def actualizar_usuario(id_usuario: int, datos):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if datos.password:
                pass_encriptada = UsuarioService.encriptar_password(datos.password)
                cursor.execute("""
                    UPDATE usuarios 
                    SET rol = ?, password = ? 
                    WHERE id_usuario = ? RETURNING id_usuario;
                """, (datos.rol, pass_encriptada, id_usuario))
            else:
                cursor.execute("""
                    UPDATE usuarios 
                    SET rol = ? 
                    WHERE id_usuario = ? RETURNING id_usuario;
                """, (datos.rol, id_usuario))
            
            actualizado = cursor.fetchone()
            conn.commit()
            return dict(actualizado) if actualizado else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()