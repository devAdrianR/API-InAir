from datetime import date
from pydantic import BaseModel
from typing import Optional

class Dispositivo(BaseModel):
    id: Optional[int] = None
    id_salon: int
    codigo: str
    modelo: Optional[str] = None
    fecha_instalacion: Optional[date] = None