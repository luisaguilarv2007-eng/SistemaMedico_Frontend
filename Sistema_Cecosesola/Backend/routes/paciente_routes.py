from fastapi import APIRouter
from controllers.paciente_controller import PacienteController
from models.paciente_dto import PacienteCreate, PacienteUpdate

router = APIRouter(prefix="/api/pacientes", tags=["Pacientes"])

@router.get("/")
def listar_pacientes():
    return PacienteController.get_pacientes()

@router.post("/", status_code=201)
def registrar_paciente(paciente: PacienteCreate):
    return PacienteController.create_paciente(paciente)

@router.delete("/{cedula}")
def inhabilitar_paciente(cedula: str):
    return PacienteController.delete_paciente(cedula)

@router.put("/{cedula}")
def actualizar_paciente(cedula: str, paciente: PacienteUpdate):
    return PacienteController.update_paciente(cedula, paciente)