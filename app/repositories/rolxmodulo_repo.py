from app.core.database import Database

class RolxModuloRepository:
    def __init__(self):
        self.db = Database()

    def obtener_modulos_por_rol(self, id_rol: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.nombre, m.ruta, m.icono
            FROM rolxmodulo rm
            JOIN modulo m ON m.id = rm.id_modulo
            WHERE rm.id_rol = %s AND rm.estado = 1 AND m.estado = 1
            ORDER BY m.id ASC;
        """, (id_rol,))
        modulos = cursor.fetchall()
        conn.close()
        return modulos