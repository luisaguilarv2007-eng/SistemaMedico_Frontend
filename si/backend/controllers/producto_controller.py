from fastapi import HTTPException
from models.producto import ProductoCreate, ProductoUpdate
from services.producto_service import ProductoService

class ProductoController:
    # Capa de Controladores: Recibe Request desde las rutas, orquesta llamadas a la capa de servicios, retorna Response
    
    @staticmethod
    def get_productos():
        """Controlador para listar productos activos."""
        return ProductoService.get_all_active_productos()

    @staticmethod
    def get_producto(producto_id: int):
        """Controlador para obtener un producto."""
        producto = ProductoService.get_producto_by_id(producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto

    @staticmethod
    def create_producto(data: ProductoCreate):
        """Controlador para crear un producto."""
        try:
            return ProductoService.create_producto(data)
        except ValueError as e:
            # Errores de validación o negocio se devuelven como 400 Bad Request
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def update_producto(producto_id: int, data: ProductoUpdate):
        """Controlador para actualizar un producto."""
        try:
            producto = ProductoService.update_producto(producto_id, data)
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            return producto
        except ValueError as e:
            # Errores de entidad procesable se devuelven como 422 Unprocessable Entity
            raise HTTPException(status_code=422, detail=str(e))

    @staticmethod
    def delete_producto(producto_id: int):
        """Controlador para borrar lógicamente un producto."""
        success = ProductoService.soft_delete_producto(producto_id)
        if not success:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"mensaje": "Producto eliminado correctamente (soft delete)"}

    @staticmethod
    def get_categorias():
        """Controlador para obtener todas las categorías."""
        return ProductoService.get_all_categorias()

    @staticmethod
    def create_categoria(data: dict):
        """Controlador para crear una categoría."""
        nombre = data.get("nombre")
        if not nombre:
            raise HTTPException(status_code=400, detail="El nombre de la categoría es requerido.")
        try:
            return ProductoService.create_categoria(nombre)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
