from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import requiere_roles
from app.models.dispositivo import Dispositivo
from app.repositories.dispositivo_repo import DispositivoRepository

router = APIRouter(
    prefix="/dispositivos",
    tags=["Gestión de Dispositivos"],
    dependencies=[Depends(requiere_roles("Administrador"))]
)
repo = DispositivoRepository()

@router.get("/")
def listar_dispositivos():
    return repo.obtener_todos()

@router.get("/{dispositivo_id}")
def obtener_dispositivo(dispositivo_id: int):
    dato = repo.obtener_por_id(dispositivo_id)
    if not dato:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return dato

@router.post("/")
def crear_dispositivo(dispositivo: Dispositivo):
    try:
        nuevo_id = repo.crear(dispositivo)
    except ValueError:
        raise HTTPException(status_code=409, detail="Ya existe un dispositivo con ese código")
    return {"mensaje": "Dispositivo registrado exitosamente", "id": nuevo_id}

@router.put("/{dispositivo_id}")
def actualizar_dispositivo(dispositivo_id: int, dispositivo: Dispositivo):
    try:
        exito = repo.actualizar(dispositivo_id, dispositivo)
    except ValueError:
        raise HTTPException(status_code=409, detail="Ya existe un dispositivo con ese código")
    if not exito:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return {"mensaje": "Dispositivo actualizado correctamente"}

@router.delete("/{dispositivo_id}")
def eliminar_dispositivo(dispositivo_id: int):
    if not repo.eliminar(dispositivo_id):
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return {"mensaje": "Dispositivo eliminado correctamente"}