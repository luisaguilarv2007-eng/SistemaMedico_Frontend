from pydantic import BaseModel
from typing import Optional
from datetime import date

class PacienteCreate(BaseModel):
    cedula_paci: str
    nombre_completo: str
    fecha_naci: date
    sexo: str
    telefono: str
    correo: Optional[str] = None
    direccion: Optional[str] = None

class PacienteUpdate(BaseModel):
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None