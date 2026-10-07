from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

# ================================
# Modelos (DTOs) para Categorías
# ================================
class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# ================================
# Modelos (DTOs) para Productos
# ================================
class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, description="El nombre no puede estar vacío")
    descripcion: Optional[str] = None
    categoria_id: int
    precio: float = Field(..., gt=0, description="El precio debe ser positivo")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

class Producto(ProductoBase):
    id: int
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)
