from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import requiere_roles
from app.models.sensor import Sensor
from app.repositories.sensor_repo import SensorRepository

router = APIRouter(
    prefix="/sensores",
    tags=["Gestión de Sensores"],
    dependencies=[Depends(requiere_roles("Administrador"))]
)
repo = SensorRepository()

@router.get("/")
def listar_sensores():
    return repo.obtener_todos()

@router.get("/{sensor_id}")
def obtener_sensor(sensor_id: int):
    dato = repo.obtener_por_id(sensor_id)
    if not dato:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return dato

@router.post("/")
def crear_sensor(sensor: Sensor):
    nuevo_id = repo.crear(sensor)
    return {"mensaje": "Sensor registrado exitosamente", "id": nuevo_id}

@router.put("/{sensor_id}")
def actualizar_sensor(sensor_id: int, sensor: Sensor):
    if not repo.actualizar(sensor_id, sensor):
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return {"mensaje": "Sensor actualizado correctamente"}

@router.delete("/{sensor_id}")
def eliminar_sensor(sensor_id: int):
    if not repo.eliminar(sensor_id):
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return {"mensaje": "Sensor eliminado correctamente"}