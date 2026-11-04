from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import requiere_roles
from app.repositories.alerta_repo import AlertaRepository

router = APIRouter(
    prefix="/alertas",
    tags=["Gestión de Alertas"],
    dependencies=[Depends(requiere_roles("Administrador", "Técnico"))]
)
repo = AlertaRepository()

@router.get("/")
def listar_alertas():
    return repo.obtener_todos()

@router.get("/{alerta_id}")
def obtener_alerta(alerta_id: int):
    alerta = repo.obtener_por_id(alerta_id)
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alerta

@router.put("/{alerta_id}/atender")
def atender_alerta(alerta_id: int):
    if not repo.marcar_atendida(alerta_id):
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": "Alerta marcada como atendida"}

@router.delete("/{alerta_id}", dependencies=[Depends(requiere_roles("Administrador"))])
def eliminar_alerta(alerta_id: int):
    if not repo.eliminar(alerta_id):
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": "Alerta eliminada correctamente"}