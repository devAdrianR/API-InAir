from pydantic import BaseModel
from typing import Optional

class Salon(BaseModel):
    id: Optional[int] = None
    id_sede: int
    nombre: str
    piso: Optional[int] = None
    capacidad: Optional[int] = None