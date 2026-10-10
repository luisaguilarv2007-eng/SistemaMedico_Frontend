from fastapi import APIRouter
from controllers.distribucion_controller import DistribucionController
from models.distribucion_dto import ArchivoCreate, EnvioCreate, EnvioUpdate

router = APIRouter(prefix="/api/distribucion", tags=["Distribución de Resultados"])

# Rutas para Archivos
@router.post("/adjuntos", status_code=201)
def subir_pdf(archivo: ArchivoCreate):
    return DistribucionController.upload_archivo(archivo)

@router.delete("/adjuntos/{id_archivo}")
def borrar_pdf_erroneo(id_archivo: int):
    return DistribucionController.delete_archivo(id_archivo)

# Rutas para Envíos
@router.post("/envios", status_code=201)
def programar_notificacion(envio: EnvioCreate):
    return DistribucionController.crear_envio(envio)

@router.put("/envios/{id_envio}")
def actualizar_notificacion(id_envio: int, datos: EnvioUpdate):
    return DistribucionController.update_envio(id_envio, datos)