from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import requiere_roles
from app.models.sede import Sede
from app.repositories.sede_repo import SedeRepository

router = APIRouter(
    prefix="/sedes",
    tags=["Gestión de Sedes"],
    dependencies=[Depends(requiere_roles("Administrador"))]
)
repo = SedeRepository()

@router.get("/")
def listar_sedes():
    return repo.obtener_todos()

@router.get("/{sede_id}")
def obtener_sede(sede_id: int):
    sede = repo.obtener_por_id(sede_id)
    if not sede:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return sede

@router.post("/")
def crear_sede(sede: Sede):
    nuevo_id = repo.crear(sede)
    return {"mensaje": "Sede registrada exitosamente", "id": nuevo_id}

@router.put("/{sede_id}")
def actualizar_sede(sede_id: int, sede: Sede):
    if not repo.actualizar(sede_id, sede):
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return {"mensaje": "Sede actualizada correctamente"}

@router.delete("/{sede_id}")
def eliminar_sede(sede_id: int):
    if not repo.eliminar(sede_id):
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return {"mensaje": "Sede eliminada correctamente"}