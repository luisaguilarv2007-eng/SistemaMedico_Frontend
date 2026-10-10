from fastapi import HTTPException
from services.catalogo_service import CatalogoService
from models.catalogo_dto import CatalogoCreate, CatalogoUpdate

class CatalogoController:
    @staticmethod
    def get_servicios():
        return CatalogoService.obtener_todos()

    @staticmethod
    def create_servicio(servicio_data: CatalogoCreate):
        try:
            return CatalogoService.crear_servicio(servicio_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def update_servicio(id_servicio: int, servicio_data: CatalogoUpdate):
        resultado = CatalogoService.actualizar_servicio(id_servicio, servicio_data)
        if not resultado:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        return {"mensaje": "Catálogo actualizado correctamente"}

    @staticmethod
    def delete_servicio(id_servicio: int):
        resultado = CatalogoService.inhabilitar_servicio(id_servicio)
        if not resultado:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        return {"mensaje": "Servicio inhabilitado del catálogo"}