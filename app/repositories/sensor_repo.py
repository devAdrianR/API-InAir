from app.core.database import Database
from app.models.sensor import Sensor

class SensorRepository:
    CONSULTA = """
        SELECT s.id, s.id_dispositivo, d.codigo AS dispositivo, s.tipo,
               s.unidad, s.modelo, s.estado, s.creado, s.actualizado
        FROM sensor s
        JOIN dispositivo d ON d.id = s.id_dispositivo
        WHERE s.estado = 1
    """

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(self.CONSULTA + " ORDER BY s.id ASC;")
        datos = cursor.fetchall()
        conn.close()
        return datos

    def obtener_por_id(self, sensor_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(self.CONSULTA + " AND s.id = %s;", (sensor_id,))
        dato = cursor.fetchone()
        conn.close()
        return dato

    def crear(self, s: Sensor):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sensor (id_dispositivo, tipo, unidad, modelo)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (s.id_dispositivo, s.tipo, s.unidad, s.modelo))
        nuevo_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, sensor_id: int, s: Sensor):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sensor SET id_dispositivo = %s, tipo = %s, unidad = %s, modelo = %s
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (s.id_dispositivo, s.tipo, s.unidad, s.modelo, sensor_id))
        resultado = cursor.fetchone()
        conn.commit()
        conn.close()
        return resultado is not None

    def eliminar(self, sensor_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sensor SET estado = 0
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (sensor_id,))
        resultado = cursor.fetchone()
        conn.commit()
        conn.close()
        return resultado is not None