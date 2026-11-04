from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import seguridad, usuario_actual
from app.models.auth import LoginRequest
from app.repositories.usuario_repo import UsuarioRepository
from app.repositories.rolxmodulo_repo import RolxModuloRepository

router = APIRouter(prefix="/auth", tags=["Autenticación"])
usuario_repo = UsuarioRepository()
rolxmodulo_repo = RolxModuloRepository()

@router.post("/login")
def login(datos: LoginRequest):
    usuario = usuario_repo.obtener_por_correo(datos.correo)

    if not usuario or not seguridad.verificar_contrasena(
        datos.contrasena, usuario["contrasena"]
    ):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    token = seguridad.crear_token({
        "id_usuario": usuario["id"],
        "id_rol": usuario["id_rol"],
        "rol": usuario["rol"],
    })

    modulos = rolxmodulo_repo.obtener_modulos_por_rol(usuario["id_rol"])

    return {
        "token": token,
        "tipo": "bearer",
        "usuario": {
            "nombres": usuario["nombres"],
            "apellidos": usuario["apellidos"],
            "correo": usuario["correo"],
            "rol": usuario["rol"],
        },
        "modulos": modulos,
    }

@router.get("/menu")
def menu(actual: dict = Depends(usuario_actual)):
    return rolxmodulo_repo.obtener_modulos_por_rol(actual["id_rol"])