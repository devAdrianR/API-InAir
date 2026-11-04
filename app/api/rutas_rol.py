from fastapi import APIRouter, Depends, HTTPException
from app.models.rol import Rol
from app.repositories.rol_repo import RolRepository
from app.core.seguridad import requiere_roles

router = APIRouter(
    prefix="/roles",
    tags=["Gestión de Roles"],
    dependencies=[Depends(requiere_roles("Administrador"))]
)

repo = RolRepository()

@router.get("/")
def listar_roles():
    return repo.obtener_todos()

@router.get("/{rol_id}")
def obtener_rol(rol_id: int):
    rol = repo.obtener_por_id(rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.post("/")
def crear_rol(rol: Rol):
    nuevo_id = repo.crear(rol)
    return {"mensaje": "Rol registrado exitosamente", "id": nuevo_id}

@router.put("/{rol_id}")
def actualizar_rol(rol_id: int, rol: Rol):
    if not repo.actualizar(rol_id, rol):
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"mensaje": "Rol actualizado correctamente"}

@router.delete("/{rol_id}")
def eliminar_rol(rol_id: int):
    if not repo.eliminar(rol_id):
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"mensaje": "Rol eliminado correctamente"}