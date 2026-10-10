from pydantic import BaseModel
from typing import Optional

class UsuarioCreate(BaseModel):
    nombre: str
    password: str
    rol: str

class UsuarioLogin(BaseModel):
    nombre: str
    password: str

class UsuarioUpdate(BaseModel):
    rol: Optional[str] = None
    password: Optional[str] = None