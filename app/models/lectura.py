from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Lectura(BaseModel):
    id: Optional[int] = None
    id_sensor: int
    valor: float
    fecha_lectura: Optional[datetime] = None