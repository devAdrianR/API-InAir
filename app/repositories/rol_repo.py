from app.core.database import Database
from app.models.rol import Rol

class RolRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, estado, creado, actualizado
            FROM rol WHERE estado = 1 ORDER BY id ASC;
        """)
        roles = cursor.fetchall()
        conn.close()
        return roles

    def obtener_por_id(self, rol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, estado, creado, actualizado
            FROM rol WHERE id = %s AND estado = 1;
        """, (rol_id,))
        rol = cursor.fetchone()
        conn.close()
        return rol

    def crear(self, rol: Rol):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rol (nombre, descripcion)
            VALUES (%s, %s) RETURNING id;
        """, (rol.nombre, rol.descripcion))
        nuevo_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, rol_id: int, rol: Rol):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE rol SET nombre = %s, descripcion = %s
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (rol.nombre, rol.descripcion, rol_id))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, rol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE rol SET estado = 0
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (rol_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None