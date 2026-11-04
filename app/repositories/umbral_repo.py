from app.core.database import Database
from app.models.umbral import Umbral

class UmbralRepository:
    COLUMNAS = """id, tipo_medicion, valor_minimo, valor_maximo, nivel,
                  estado, creado, actualizado"""

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT {self.COLUMNAS} FROM umbral WHERE estado = 1 ORDER BY id ASC;")
        datos = cursor.fetchall()
        conn.close()
        return datos

    def obtener_por_id(self, umbral_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT {self.COLUMNAS} FROM umbral WHERE id = %s AND estado = 1;", (umbral_id,))
        dato = cursor.fetchone()
        conn.close()
        return dato

    def crear(self, u: Umbral):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO umbral (tipo_medicion, valor_minimo, valor_maximo, nivel)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (u.tipo_medicion, u.valor_minimo, u.valor_maximo, u.nivel))
        nuevo_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, umbral_id: int, u: Umbral):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE umbral SET tipo_medicion = %s, valor_minimo = %s,
                   valor_maximo = %s, nivel = %s
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (u.tipo_medicion, u.valor_minimo, u.valor_maximo, u.nivel, umbral_id))
        resultado = cursor.fetchone()
        conn.commit()
        conn.close()
        return resultado is not None

    def eliminar(self, umbral_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE umbral SET estado = 0
            WHERE id = %s AND estado = 1 RETURNING id;
        """, (umbral_id,))
        resultado = cursor.fetchone()
        conn.commit()
        conn.close()
        return resultado is not None