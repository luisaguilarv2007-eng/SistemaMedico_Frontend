from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import paciente_routes, usuarios_routes, catalogo_routes, orden_routes, distribucion_routes
app = FastAPI(title="API CECOCESOLA - InfoLab")

# Configuración CORS para que el Frontend (React/JS) pueda consumir la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejo Global de Errores: Atrapa excepciones sin tumbar el servidor
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"mensaje": "Error interno del servidor", "detalle": repr(exc)}, # <-- Aquí está el cambio clave
    )

# Integración de la Capa de Rutas
app.include_router(paciente_routes.router)
app.include_router(usuarios_routes.router)
app.include_router(catalogo_routes.router)
app.include_router(orden_routes.router)
app.include_router(distribucion_routes.router)
# Iniciar servidor: uvicorn main:app --reload