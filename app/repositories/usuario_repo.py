import psycopg2
from app.core.database import Database
from app.core.seguridad import seguridad
from app.models.usuario import Usuario

class UsuarioRepository:
    def __init__(self):
        self.db = Database()

    # Usado por el login
    def obtener_por_correo(self, correo: str):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.id_rol, u.nombres, u.apellidos, u.correo,
                   u.contrasena, r.nombre AS rol
            FROM usuario u
            JOIN rol r ON r.id = u.id_rol
            WHERE u.correo = %s AND u.estado = 1 AND r.estado = 1;
        """, (correo,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.id_rol, r.nombre AS rol, u.nombres, u.apellidos,
                   u.correo, u.telefono, u.estado, u.creado, u.actualizado
            FROM usuario u
            JOIN rol r ON r.id = u.id_rol
            WHERE u.estado = 1
            ORDER BY u.id ASC;
        """)
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    def obtener_por_id(self, usuario_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.id_rol, r.nombre AS rol, u.nombres, u.apellidos,
                   u.correo, u.telefono, u.estado, u.creado, u.actualizado
            FROM usuario u
            JOIN rol r ON r.id = u.id_rol
            WHERE u.id = %s AND u.estado = 1;
        """, (usuario_id,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    def crear(self, usuario: Usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuario (id_rol, nombres, apellidos, correo, contrasena, telefono)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """, (usuario.id_rol, usuario.nombres, usuario.apellidos, usuario.correo,
                  seguridad.hashear_contrasena(usuario.contrasena), usuario.telefono))
            nuevo_id = cursor.fetchone()['id']
            conn.commit()
            return nuevo_id
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise ValueError("correo duplicado")
        finally:
            conn.close()

    def actualizar(self, usuario_id: int, usuario: Usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            if usuario.contrasena:
                cursor.execute("""
                    UPDATE usuario SET id_rol = %s, nombres = %s, apellidos = %s,
                        correo = %s, telefono = %s, contrasena = %s
                    WHERE id = %s AND estado = 1 RETURNING id;
                """, (usuario.id_rol, usuario.nombres, usuario.apellidos, usuario.correo,
                      usuario.telefono, seguridad.hashear_contrasena(usuario.contrasena),
                      usuario_id))
            else:
                cursor.execute("""
                    UPDATE usuario SET id_rol = %s, nombres = %s, apellidos = %s,
                        correo = %s, telefono = %s
                    WHERE id = %s AND estado = 1 RETURNING id;
                """, (usuario.id_rol, usuario.nombres, usuario.apellidos, usuario.correo,
                      usuario.telefono, usuario_id))
            actualizado = cursor.fetchone()
            conn.commit()
            return actualizado is not None
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise ValueError("correo duplicado")
        finally:
            conn.close()

    def eliminar(self, usuario_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuario SET estado = 0
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (usuario_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None