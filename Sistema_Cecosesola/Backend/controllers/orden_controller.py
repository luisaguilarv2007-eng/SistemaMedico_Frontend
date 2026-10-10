from fastapi import HTTPException
from services.orden_service import OrdenService
from models.orden_dto import OrdenCreate, DetalleUpdate

class OrdenController:
    @staticmethod
    def get_ordenes_pendientes():
        return OrdenService.obtener_lista_espera()

    @staticmethod
    def create_orden(orden_data: OrdenCreate):
        try:
            return OrdenService.crear_orden_completa(orden_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def procesar_resultados(id_detalle: int, detalle_data: DetalleUpdate):
        try:
            resultado = OrdenService.cargar_resultados_json(id_detalle, detalle_data)
            if not resultado:
                raise HTTPException(status_code=404, detail="Detalle de orden no encontrado")
            return {"mensaje": "Resultados de laboratorio guardados exitosamente"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))