from app.core.database import Database

class AlertaRepository:
    CONSULTA = """
        SELECT a.id, sa.nombre AS salon, sd.nombre AS sede, s.tipo AS sensor,
               l.valor, s.unidad, u.nivel, a.mensaje, a.atendida,
               l.fecha_lectura, a.estado, a.creado, a.actualizado
        FROM alerta a
        JOIN lectura l     ON l.id  = a.id_lectura
        JOIN sensor s      ON s.id  = l.id_sensor
        JOIN dispositivo d ON d.id  = s.id_dispositivo
        JOIN salon sa      ON sa.id = d.id_salon
        JOIN sede sd       ON sd.id = sa.id_sede
        JOIN umbral u      ON u.id  = a.id_umbral
        WHERE a.estado = 1
    """

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(self.CONSULTA + " ORDER BY a.id DESC;")
        alertas = cursor.fetchall()
        conn.close()
        return alertas

    def obtener_por_id(self, alerta_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(self.CONSULTA + " AND a.id = %s;", (alerta_id,))
        alerta = cursor.fetchone()
        conn.close()
        return alerta

    def marcar_atendida(self, alerta_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE alerta SET atendida = 1
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (alerta_id,))
        resultado = cursor.fetchone()
        conn.commit()
        conn.close()
        return resultado is not None

    def eliminar(self, alerta_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE alerta SET estado = 0
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (alerta_id,))
        eliminado = cursor.fetchone()
        conn.commit()
        conn.close()
        return eliminado is not None