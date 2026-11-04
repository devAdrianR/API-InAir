from pydantic import BaseModel
from typing import Optional

class Umbral(BaseModel):
    id: Optional[int] = None
    tipo_medicion: str
    valor_minimo: Optional[float] = None
    valor_maximo: Optional[float] = None
    nivel: str