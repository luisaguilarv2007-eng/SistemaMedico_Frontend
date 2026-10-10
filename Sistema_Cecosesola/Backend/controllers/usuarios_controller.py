from fastapi import HTTPException
from services.usuarios_service import UsuarioService
from models.usuarios_dto import UsuarioCreate, UsuarioLogin, UsuarioUpdate

class UsuarioController:
    @staticmethod
    def get_usuarios():
        return UsuarioService.obtener_todos()

    @staticmethod
    def create_usuario(usuario_data: UsuarioCreate):
        try:
            return UsuarioService.crear_usuario(usuario_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def login_usuario(credenciales: UsuarioLogin):
        usuario = UsuarioService.validar_login(credenciales.nombre_usuario, credenciales.contrasena)
        if not usuario:
            # Error 401: Unauthorized (Credenciales inválidas)
            raise HTTPException(status_code=401, detail="Credenciales incorrectas o usuario inactivo")
        return {"mensaje": "Inicio de sesión exitoso", "usuario": usuario}

    @staticmethod
    def delete_usuario(id_usuario: int):
        resultado = UsuarioService.inhabilitar_usuario(id_usuario)
        if not resultado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"mensaje": "Usuario inhabilitado correctamente"}
    
    @staticmethod
    def update_usuario(id_usuario: int, usuario_data: UsuarioUpdate):
        resultado = UsuarioService.actualizar_usuario(id_usuario, usuario_data)
        if not resultado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"mensaje": "Acceso modificado correctamente"}