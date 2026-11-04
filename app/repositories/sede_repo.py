from app.core.database import Database
from app.models.sede import Sede

class SedeRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, direccion, ciudad, estado, creado, actualizado
            FROM sede WHERE estado = 1 ORDER BY id ASC;
        """)
        sedes = cursor.fetchall()
        conn.close()
        return sedes

    def obtener_por_id(self, sede_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, direccion, ciudad, estado, creado, actualizado
            FROM sede WHERE id = %s AND estado = 1;
        """, (sede_id,))
        sede = cursor.fetchone()
        conn.close()
        return sede

    def crear(self, sede: Sede):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sede (nombre, direccion, ciudad)
            VALUES (%s, %s, %s) RETURNING id;
        """, (sede.nombre, sede.direccion, sede.ciudad))
        nuevo_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, sede_id: int, sede: Sede):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sede SET nombre = %s, direccion = %s, ciudad = %s
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (sede.nombre, sede.direccion, sede.ciudad, sede_id))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, sede_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sede SET estado = 0
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (sede_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None