
from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import requiere_roles
from app.models.sensor import Sensor
from app.repositories.sensor_repo import SensorRepository

router = APIRouter(
    prefix="/sensores",
    tags=["Gestión de Sensores"]
)

repo = SensorRepository()

# Administrador y Técnico pueden consultar sensores
@router.get("/", dependencies=[Depends(requiere_roles("Administrador", "Tecnico"))])
def listar_sensores():
    return repo.obtener_todos()

@router.get("/{sensor_id}", dependencies=[Depends(requiere_roles("Administrador", "Tecnico"))])
def obtener_sensor(sensor_id: int):
    dato = repo.obtener_por_id(sensor_id)
    if not dato:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return dato

# Solamente Administrador puede gestionar sensores
@router.post("/", dependencies=[Depends(requiere_roles("Administrador"))])
def crear_sensor(sensor: Sensor):
    nuevo_id = repo.crear(sensor)
    return {"mensaje": "Sensor registrado exitosamente", "id": nuevo_id}

@router.put("/{sensor_id}", dependencies=[Depends(requiere_roles("Administrador"))])
def actualizar_sensor(sensor_id: int, sensor: Sensor):
    if not repo.actualizar(sensor_id, sensor):
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return {"mensaje": "Sensor actualizado correctamente"}

@router.delete("/{sensor_id}", dependencies=[Depends(requiere_roles("Administrador"))])
def eliminar_sensor(sensor_id: int):
    if not repo.eliminar(sensor_id):
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return {"mensaje": "Sensor eliminado correctamente"}
