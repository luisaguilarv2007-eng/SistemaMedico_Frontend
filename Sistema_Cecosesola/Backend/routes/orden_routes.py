from fastapi import APIRouter
from controllers.orden_controller import OrdenController
from models.orden_dto import OrdenCreate, DetalleUpdate

router = APIRouter(prefix="/api/ordenes", tags=["Órdenes y Facturación"])

@router.get("/espera")
def listar_cola_espera():
    return OrdenController.get_ordenes_pendientes()

@router.post("/", status_code=201)
def procesar_nueva_orden(orden: OrdenCreate):
    return OrdenController.create_orden(orden)

@router.put("/detalle/{id_detalle}/resultados")
def cargar_resultados(id_detalle: int, datos: DetalleUpdate):
    return OrdenController.procesar_resultados(id_detalle, datos)