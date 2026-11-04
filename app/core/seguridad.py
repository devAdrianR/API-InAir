import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

esquema = HTTPBearer()

class Seguridad:
    def __init__(self):
        self.secreto = os.getenv("JWT_SECRET")
        self.algoritmo = os.getenv("JWT_ALGORITHM", "HS256")
        self.minutos = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    def verificar_contrasena(self, plana: str, hash_guardado: str) -> bool:
        return bcrypt.checkpw(plana.encode("utf-8"), hash_guardado.encode("utf-8"))

    def crear_token(self, datos: dict) -> str:
        contenido = datos.copy()
        contenido["exp"] = datetime.now(timezone.utc) + timedelta(minutes=self.minutos)
        return jwt.encode(contenido, self.secreto, algorithm=self.algoritmo)

    def hashear_contrasena(self, plana: str) -> str:
        return bcrypt.hashpw(plana.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    
    def decodificar_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secreto, algorithms=[self.algoritmo])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="El token expiró")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")

seguridad = Seguridad()

def usuario_actual(credenciales: HTTPAuthorizationCredentials = Depends(esquema)):
    return seguridad.decodificar_token(credenciales.credentials)

def requiere_roles(*roles_permitidos):
    def verificador(actual: dict = Depends(usuario_actual)):
        if actual["rol"] not in roles_permitidos:
            raise HTTPException(status_code=403, detail="No tienes permiso para esta acción")
        return actual
    return verificador

