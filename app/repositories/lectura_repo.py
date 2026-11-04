from app.core.database import Database
from app.models.lectura import Lectura

class LecturaRepository:
    CONSULTA = """
        SELECT l.id, l.id_sensor, sa.nombre AS salon, se.nombre AS sede,
               s.tipo AS sensor, l.valor, s.unidad, l.fecha_lectura,
               l.estado, l.creado, l.actualizado
        FROM lectura l
        JOIN sensor s      ON s.id  = l.id_sensor
        JOIN dispositivo d ON d.id  = s.id_dispositivo
        JOIN salon sa      ON sa.id = d.id_salon
        JOIN sede se       ON se.id = sa.id_sede
        WHERE l.estado = 1
    """

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(self.CONSULTA + " ORDER BY l.fecha_lectura DESC, l.id DESC LIMIT 200;")
        datos = cursor.fetchall()
        conn.close()
        return datos

    def obtener_por_id(self, lectura_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(self.CONSULTA + " AND l.id = %s;", (lectura_id,))
        dato = cursor.fetchone()
        conn.close()
        return dato

    def crear(self, lectura: Lectura):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # 1. El sensor debe existir
            cursor.execute(
                "SELECT tipo, unidad FROM sensor WHERE id = %s AND estado = 1;",
                (lectura.id_sensor,)
            )
            sensor = cursor.fetchone()
            if not sensor:
                raise LookupError("sensor no encontrado")

            # 2. Guardar la lectura
            cursor.execute("""
                INSERT INTO lectura (id_sensor, valor, fecha_lectura)
                VALUES (%s, %s, COALESCE(%s::timestamp, NOW())) RETURNING id;
            """, (lectura.id_sensor, lectura.valor, lectura.fecha_lectura))
            lectura_id = cursor.fetchone()['id']

            # 3. Buscar el umbral que le corresponde al valor
            cursor.execute("""
                SELECT id, nivel FROM umbral
                WHERE tipo_medicion = %s AND estado = 1 AND valor_minimo <= %s
                ORDER BY valor_minimo DESC LIMIT 1;
            """, (sensor['tipo'], lectura.valor))
            umbral = cursor.fetchone()

            # 4. Si no es Normal, crear la alerta
            alerta_generada = False
            if umbral and umbral['nivel'] != 'Normal':
                texto = "en nivel crítico" if umbral['nivel'] == 'Crítico' else "en precaución"
                mensaje = f"{sensor['tipo']} {texto}: {lectura.valor:g} {sensor['unidad'] or ''}".strip()
                cursor.execute("""
                    INSERT INTO alerta (id_lectura, id_umbral, mensaje)
                    VALUES (%s, %s, %s);
                """, (lectura_id, umbral['id'], mensaje))
                alerta_generada = True

            conn.commit()
            return {"id": lectura_id, "alerta_generada": alerta_generada}
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def eliminar(self, lectura_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE lectura SET estado = 0
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (lectura_id,))
        resultado = cursor.fetchone()
        conn.commit()
        conn.close()
        return resultado is not None