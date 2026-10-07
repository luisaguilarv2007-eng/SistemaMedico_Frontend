from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Callable

# Middleware global para manejar excepciones y asegurar que la API no se detenga por errores inesperados
async def global_error_handler(request: Request, call_next: Callable):
    try:
        # Pasa la solicitud al siguiente proceso en el pipeline (las rutas/controladores)
        response = await call_next(request)
        return response
    except Exception as exc:
        # En caso de error crítico no manejado, retorna un estado 500 y previene la caída del servidor
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Ocurrió un error interno en el servidor", "error": str(exc)}
        )
