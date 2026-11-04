from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int] = None
    id_rol: int
    nombres: str
    apellidos: str
    correo: str
    contrasena: Optional[str] = None
    telefono: Optional[str] = None