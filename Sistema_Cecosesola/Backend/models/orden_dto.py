from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ServicioOrden(BaseModel):
    id_servicio: int

class OrdenCreate(BaseModel):
    cedula_paci: str
    id_medico_tratante: int
    servicios: List[ServicioOrden]  # Arreglo con los estudios solicitados
    
    # Datos para facturación y pago
    tipo_documento: str
    razon_social: str
    subtotal: float
    iva: float
    monto_total: float
    id_cajero: int
    metodo_pago: int
    referencia: Optional[str] = None

class DetalleUpdate(BaseModel):
    # DTO para cuando el Bioanalista cargue los resultados en JSONB
    id_usuario_procesa: int
    datos_laboratorio: Dict[str, Any]
    estado_examen: str  # Ej: 'Procesado' o 'Validado'