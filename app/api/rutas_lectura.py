from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import requiere_roles, usuario_actual
from app.models.lectura import Lectura
from app.repositories.lectura_repo import LecturaRepository

router = APIRouter(prefix="/lecturas", tags=["Gestión de Lecturas"])
repo = LecturaRepository()

@router.get("/", dependencies=[Depends(usuario_actual)])
def listar_lecturas():
    return repo.obtener_todos()

@router.get("/{lectura_id}", dependencies=[Depends(usuario_actual)])
def obtener_lectura(lectura_id: int):
    dato = repo.obtener_por_id(lectura_id)
    if not dato:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return dato

@router.post("/", dependencies=[Depends(requiere_roles("Administrador", "Técnico"))])
def crear_lectura(lectura: Lectura):
    try:
        resultado = repo.crear(lectura)
    except LookupError:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return {"mensaje": "Lectura registrada exitosamente", **resultado}

@router.delete("/{lectura_id}", dependencies=[Depends(requiere_roles("Administrador"))])
def eliminar_lectura(lectura_id: int):
    if not repo.eliminar(lectura_id):
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return {"mensaje": "Lectura eliminada correctamente"}