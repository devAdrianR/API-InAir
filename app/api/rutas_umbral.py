from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import requiere_roles
from app.models.umbral import Umbral
from app.repositories.umbral_repo import UmbralRepository

router = APIRouter(
    prefix="/umbrales",
    tags=["Gestión de Umbrales"],
    dependencies=[Depends(requiere_roles("Administrador"))]
)
repo = UmbralRepository()

@router.get("/")
def listar_umbrales():
    return repo.obtener_todos()

@router.get("/{umbral_id}")
def obtener_umbral(umbral_id: int):
    dato = repo.obtener_por_id(umbral_id)
    if not dato:
        raise HTTPException(status_code=404, detail="Umbral no encontrado")
    return dato

@router.post("/")
def crear_umbral(umbral: Umbral):
    nuevo_id = repo.crear(umbral)
    return {"mensaje": "Umbral registrado exitosamente", "id": nuevo_id}

@router.put("/{umbral_id}")
def actualizar_umbral(umbral_id: int, umbral: Umbral):
    if not repo.actualizar(umbral_id, umbral):
        raise HTTPException(status_code=404, detail="Umbral no encontrado")
    return {"mensaje": "Umbral actualizado correctamente"}

@router.delete("/{umbral_id}")
def eliminar_umbral(umbral_id: int):
    if not repo.eliminar(umbral_id):
        raise HTTPException(status_code=404, detail="Umbral no encontrado")
    return {"mensaje": "Umbral eliminado correctamente"}