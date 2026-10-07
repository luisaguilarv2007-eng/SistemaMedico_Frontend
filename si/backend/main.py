import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Importamos configuraciones y base de datos
from config import settings
from database.connection import init_db

# Importamos las rutas y middleware
from routes.productos import router as productos_router
from middleware.error_handler import global_error_handler

# ========================================================
# Inicialización de la base de datos (DDL y datos semilla)
# ========================================================
init_db()

# ========================================================
# Configuración principal de FastAPI
# ========================================================
app = FastAPI(
    title="Sistema de Gestión de Productos / Inventario",
    description="API RESTful para la gestión de productos y categorías con arquitectura por capas.",
    version="1.0.0"
)

# ========================================================
# Middlewares
# ========================================================
# Configuración de CORS para permitir el consumo desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Se permite cualquier origen para desarrollo
    allow_credentials=True,
    allow_methods=["*"], # Se permiten todos los métodos (GET, POST, etc)
    allow_headers=["*"], # Se permiten todos los headers
)

# Integración del Global Error Handler para manejo centralizado de excepciones
app.add_middleware(BaseHTTPMiddleware, dispatch=global_error_handler)

# ========================================================
# Registro de Rutas
# ========================================================
app.include_router(productos_router)

if __name__ == "__main__":
    import uvicorn
    # Inicia el servidor de Uvicorn en el puerto 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
