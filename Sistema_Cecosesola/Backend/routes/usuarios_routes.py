from fastapi import APIRouter
from controllers.usuarios_controller import UsuarioController
from models.usuarios_dto import UsuarioCreate, UsuarioLogin, UsuarioUpdate

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.get("/")
def listar_usuarios():
    return UsuarioController.get_usuarios()

@router.post("/registro", status_code=201)
def registrar_usuario(usuario: UsuarioCreate):
    return UsuarioController.create_usuario(usuario)

@router.post("/login")
def iniciar_sesion(credenciales: UsuarioLogin):
    return UsuarioController.login_usuario(credenciales)

@router.delete("/{id_usuario}")
def inhabilitar_usuario(id_usuario: int):
    return UsuarioController.delete_usuario(id_usuario)

@router.put("/{id_usuario}")
def actualizar_usuario(id_usuario: int, usuario: UsuarioUpdate):
    return UsuarioController.update_usuario(id_usuario, usuario)