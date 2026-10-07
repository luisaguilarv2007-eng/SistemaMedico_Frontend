from fastapi import APIRouter
from typing import List
from models.producto import Producto, ProductoCreate, ProductoUpdate, Categoria
from controllers.producto_controller import ProductoController

router = APIRouter()

# Capa de Rutas: Contiene endpoints REST puros con los verbos HTTP correspondientes

# --- Endpoints de Productos ---

@router.get("/api/productos", response_model=List[Producto])
def list_productos():
    """GET /api/productos -> Lista todos los productos activos."""
    return ProductoController.get_productos()

@router.get("/api/productos/{producto_id}", response_model=Producto)
def get_producto(producto_id: int):
    """GET /api/productos/:id -> Obtiene un producto por ID."""
    return ProductoController.get_producto(producto_id)

@router.post("/api/productos", response_model=Producto, status_code=201)
def create_producto(producto: ProductoCreate):
    """POST /api/productos -> Crea un producto con validación de payload."""
    return ProductoController.create_producto(producto)

@router.put("/api/productos/{producto_id}", response_model=Producto)
def update_producto(producto_id: int, producto: ProductoUpdate):
    """PUT /api/productos/:id -> Actualiza un producto existente."""
    return ProductoController.update_producto(producto_id, producto)

@router.delete("/api/productos/{producto_id}")
def delete_producto(producto_id: int):
    """DELETE /api/productos/:id -> Borrado lógico de un producto (estado=false)."""
    return ProductoController.delete_producto(producto_id)

# --- Endpoints de Categorías ---

@router.get("/api/categorias", response_model=List[Categoria])
def list_categorias():
    """GET /api/categorias -> Lista todas las categorías."""
    return ProductoController.get_categorias()

@router.post("/api/categorias", response_model=Categoria, status_code=201)
def create_categoria(categoria: dict):
    """POST /api/categorias -> Crea una categoría."""
    return ProductoController.create_categoria(categoria)
