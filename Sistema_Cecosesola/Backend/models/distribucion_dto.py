from pydantic import BaseModel
from typing import Optional

class ArchivoCreate(BaseModel):
    id_detalle: int
    url_archivo: str # Aquí iría la ruta donde se guardó el PDF (ej. "/static/pdfs/orden_123.pdf")
    tipo_archivo: str # Ej: "application/pdf"

class EnvioCreate(BaseModel):
    id_orden: int
    canal: str # "WhatsApp" o "Correo"

class EnvioUpdate(BaseModel):
    estado_enviado: bool
    msj_error: Optional[str] = None