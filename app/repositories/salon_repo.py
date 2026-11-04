from app.core.database import Database
from app.models.salon import Salon

class SalonRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.id_sede, se.nombre AS sede, s.nombre, s.piso,
                   s.capacidad, s.estado, s.creado, s.actualizado
            FROM salon s
            JOIN sede se ON se.id = s.id_sede
            WHERE s.estado = 1
            ORDER BY s.id ASC;
        """)
        salones = cursor.fetchall()
        conn.close()
        return salones

    def obtener_por_id(self, salon_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.id_sede, se.nombre AS sede, s.nombre, s.piso,
                   s.capacidad, s.estado, s.creado, s.actualizado
            FROM salon s
            JOIN sede se ON se.id = s.id_sede
            WHERE s.id = %s AND s.estado = 1;
        """, (salon_id,))
        salon = cursor.fetchone()
        conn.close()
        return salon

    def crear(self, salon: Salon):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO salon (id_sede, nombre, piso, capacidad)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (salon.id_sede, salon.nombre, salon.piso, salon.capacidad))
        nuevo_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, salon_id: int, salon: Salon):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE salon SET id_sede = %s, nombre = %s, piso = %s, capacidad = %s
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (salon.id_sede, salon.nombre, salon.piso, salon.capacidad, salon_id))
        actualizado = cursor.fetchone()
        conn.commit()
        conn.close()
        return actualizado is not None

    def eliminar(self, salon_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE salon SET estado = 0
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (salon_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None