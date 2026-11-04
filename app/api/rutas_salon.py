from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import requiere_roles, usuario_actual
from app.models.salon import Salon
from app.repositories.salon_repo import SalonRepository

router = APIRouter(prefix="/salones", tags=["Gestión de Salones"])
repo = SalonRepository()
solo_admin = Depends(requiere_roles("Administrador"))

@router.get("/", dependencies=[Depends(usuario_actual)])
def listar_salones():
    return repo.obtener_todos()

@router.get("/{salon_id}", dependencies=[Depends(usuario_actual)])
def obtener_salon(salon_id: int):
    salon = repo.obtener_por_id(salon_id)
    if not salon:
        raise HTTPException(status_code=404, detail="Salón no encontrado")
    return salon

@router.post("/", dependencies=[solo_admin])
def crear_salon(salon: Salon):
    nuevo_id = repo.crear(salon)
    return {"mensaje": "Salón registrado exitosamente", "id": nuevo_id}

@router.put("/{salon_id}", dependencies=[solo_admin])
def actualizar_salon(salon_id: int, salon: Salon):
    if not repo.actualizar(salon_id, salon):
        raise HTTPException(status_code=404, detail="Salón no encontrado")
    return {"mensaje": "Salón actualizado correctamente"}

@router.delete("/{salon_id}", dependencies=[solo_admin])
def eliminar_salon(salon_id: int):
    if not repo.eliminar(salon_id):
        raise HTTPException(status_code=404, detail="Salón no encontrado")
    return {"mensaje": "Salón eliminado correctamente"}