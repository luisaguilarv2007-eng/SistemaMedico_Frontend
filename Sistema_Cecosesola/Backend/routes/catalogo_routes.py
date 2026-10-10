from fastapi import APIRouter
from controllers.catalogo_controller import CatalogoController
from models.catalogo_dto import CatalogoCreate, CatalogoUpdate

router = APIRouter(prefix="/api/catalogo", tags=["Catálogo de Servicios"])

@router.get("/")
def listar_servicios():
    return CatalogoController.get_servicios()

@router.post("/", status_code=201)
def registrar_servicio(servicio: CatalogoCreate):
    return CatalogoController.create_servicio(servicio)

@router.put("/{id_servicio}")
def actualizar_servicio(id_servicio: int, servicio: CatalogoUpdate):
    return CatalogoController.update_servicio(id_servicio, servicio)

@router.delete("/{id_servicio}")
def inhabilitar_servicio(id_servicio: int):
    return CatalogoController.delete_servicio(id_servicio)