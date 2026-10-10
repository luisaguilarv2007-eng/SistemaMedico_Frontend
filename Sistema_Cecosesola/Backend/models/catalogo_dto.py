from pydantic import BaseModel
from typing import Optional

class CatalogoCreate(BaseModel):
    codigo: str
    descripcion: str
    area: str
    precio: float

class CatalogoUpdate(BaseModel):
    # Opcionales para que puedan actualizar solo el precio o solo la descripción
    descripcion: Optional[str] = None
    precio: Optional[float] = None