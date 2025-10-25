from config.database import DatabaseManager

class Sucursal:
    """Modelo para la gestión de sucursales en la base de datos."""

    db = DatabaseManager()

    @classmethod
    def listar(cls):
        """
        Retorna una lista de todas las sucursales.
        
        :return: Lista de tuplas con (id, nombre, direccion, distancia_km).
        """
        query = "SELECT * FROM Sucursales"
        return cls.db.fetch_all(query)

    @classmethod
    def obtener_mas_cercana(cls):
        """
        Encuentra la sucursal con la menor distancia.
        
        :return: Tupla con los datos de la sucursal más cercana.
        """
        query = "SELECT * FROM Sucursales ORDER BY distancia_km ASC LIMIT 1"
        return cls.db.fetch_one(query)
