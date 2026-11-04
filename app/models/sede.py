from pydantic import BaseModel
from typing import Optional

class Sede(BaseModel):
    id: Optional[int] = None
    nombre: str
    direccion: Optional[str] = None
    ciudad: Optional[str] = None