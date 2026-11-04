import psycopg2
from app.core.database import Database
from app.models.dispositivo import Dispositivo

class DispositivoRepository:
    CONSULTA = """
        SELECT d.id, d.id_salon, sa.nombre AS salon, se.nombre AS sede,
               d.codigo, d.modelo, d.fecha_instalacion,
               d.estado, d.creado, d.actualizado
        FROM dispositivo d
        JOIN salon sa ON sa.id = d.id_salon
        JOIN sede se  ON se.id = sa.id_sede
        WHERE d.estado = 1
    """

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(self.CONSULTA + " ORDER BY d.id ASC;")
        datos = cursor.fetchall()
        conn.close()
        return datos

    def obtener_por_id(self, dispositivo_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(self.CONSULTA + " AND d.id = %s;", (dispositivo_id,))
        dato = cursor.fetchone()
        conn.close()
        return dato

    def crear(self, d: Dispositivo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO dispositivo (id_salon, codigo, modelo, fecha_instalacion)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """, (d.id_salon, d.codigo, d.modelo, d.fecha_instalacion))
            nuevo_id = cursor.fetchone()['id']
            conn.commit()
            return nuevo_id
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise ValueError("código duplicado")
        finally:
            conn.close()

    def actualizar(self, dispositivo_id: int, d: Dispositivo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE dispositivo SET id_salon = %s, codigo = %s, modelo = %s,
                       fecha_instalacion = %s
                WHERE id = %s AND estado = 1 RETURNING id;
            """, (d.id_salon, d.codigo, d.modelo, d.fecha_instalacion, dispositivo_id))
            resultado = cursor.fetchone()
            conn.commit()
            return resultado is not None
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise ValueError("código duplicado")
        finally:
            conn.close()

    def eliminar(self, dispositivo_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE dispositivo SET estado = 0
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (dispositivo_id,))
        resultado = cursor.fetchone()
        conn.commit()
        conn.close()
        return resultado is not None