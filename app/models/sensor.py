from pydantic import BaseModel
from typing import Optional

class Sensor(BaseModel):
    id: Optional[int] = None
    id_dispositivo: int
    tipo: str
    unidad: Optional[str] = None
    modelo: Optional[str] = None