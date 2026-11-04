from fastapi import APIRouter, Depends, HTTPException
from app.core.seguridad import requiere_roles
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository

router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de Usuarios"],
    dependencies=[Depends(requiere_roles("Administrador"))]
)
repo = UsuarioRepository()

@router.get("/")
def listar_usuarios():
    return repo.obtener_todos()

@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    usuario = repo.obtener_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/")
def crear_usuario(usuario: Usuario):
    if not usuario.contrasena:
        raise HTTPException(status_code=400, detail="La contraseña es obligatoria")
    try:
        nuevo_id = repo.crear(usuario)
    except ValueError:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese correo")
    return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_id}

@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: Usuario):
    try:
        exito = repo.actualizar(usuario_id, usuario)
    except ValueError:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese correo")
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario actualizado correctamente"}

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    if not repo.eliminar(usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}