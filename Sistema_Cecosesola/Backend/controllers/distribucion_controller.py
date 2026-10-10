from fastapi import HTTPException
from services.distribucion_service import DistribucionService
from models.distribucion_dto import ArchivoCreate, EnvioCreate, EnvioUpdate

class DistribucionController:
    @staticmethod
    def upload_archivo(archivo_data: ArchivoCreate):
        try:
            return DistribucionService.guardar_adjunto(archivo_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def delete_archivo(id_archivo: int):
        resultado = DistribucionService.eliminar_adjunto(id_archivo)
        if not resultado:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        return {"mensaje": "Archivo erróneo eliminado exitosamente"}

    @staticmethod
    def crear_envio(envio_data: EnvioCreate):
        try:
            return DistribucionService.programar_envio(envio_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def update_envio(id_envio: int, envio_data: EnvioUpdate):
        resultado = DistribucionService.actualizar_estado_envio(id_envio, envio_data)
        if not resultado:
            raise HTTPException(status_code=404, detail="Registro de envío no encontrado")
        return {"mensaje": "Estatus del mensaje actualizado"}
    @staticmethod
    def get_archivos():
        return DistribucionService.obtener_archivos()

    @staticmethod
    def get_envios():
        return DistribucionService.obtener_envios()
