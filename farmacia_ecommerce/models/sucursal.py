from config.database import DatabaseManager


class Sucursal:
    db = DatabaseManager()

    @classmethod
    def listar(cls):
        query = "SELECT * FROM Sucursales"
        return cls.db.fetch_all(query)

    @classmethod
    def obtener_mas_cercana(cls):
        query = "SELECT * FROM Sucursales ORDER BY distancia_km ASC LIMIT 1"
        return cls.db.fetch_one(query)
