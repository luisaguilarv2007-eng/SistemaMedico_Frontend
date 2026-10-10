from fastapi import HTTPException
from services.paciente_service import PacienteService
from models.paciente_dto import PacienteCreate, PacienteUpdate

class PacienteController:
    @staticmethod
    def get_pacientes():
        pacientes = PacienteService.obtener_todos()
        return pacientes

    @staticmethod
    def create_paciente(paciente_data: PacienteCreate):
        try:
            resultado = PacienteService.crear_paciente(paciente_data)
            return resultado
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def delete_paciente(cedula: str):
        resultado = PacienteService.eliminar_paciente(cedula)
        if not resultado:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return {"mensaje": "Paciente inhabilitado correctamente"}
    
    @staticmethod
    def update_paciente(cedula: str, paciente_data: PacienteUpdate):
        resultado = PacienteService.actualizar_contacto(cedula, paciente_data)
        if not resultado:
            raise HTTPException(status_code=404, detail="Paciente no encontrado o inactivo")
        return {"mensaje": "Datos de contacto actualizados correctamente"}