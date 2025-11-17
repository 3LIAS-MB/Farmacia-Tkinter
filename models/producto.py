from config.database import DatabaseManager


# Modelo para la gestión de productos en la base de datos.
class Producto:
    db = DatabaseManager()

    @classmethod
    def consultar(cls, nombre):
        query = "SELECT nombre, descripcion, precio, stock FROM Productos WHERE nombre LIKE ?"
        return cls.db.fetch_all(query, (f"%{nombre}%",))

    @classmethod
    def crear(cls, nombre, descripcion, precio, stock):
        query = "INSERT INTO Productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)"
        cls.db.execute_query(query, (nombre, descripcion, precio, stock), commit=True)

    @classmethod
    def modificar(cls, prod_id, nombre, descripcion, precio, stock):
        query = "UPDATE Productos SET nombre = ?, descripcion = ?, precio = ?, stock = ? WHERE id = ?"
        cls.db.execute_query(
            query, (nombre, descripcion, precio, stock, prod_id), commit=True
        )

    @classmethod
    def eliminar(cls, prod_id):
        query = "DELETE FROM Productos WHERE id = ?"
        cls.db.execute_query(query, (prod_id,), commit=True)

    @classmethod
    def listar(cls):
        query = "SELECT * FROM Productos"
        return cls.db.fetch_all(query)

    @classmethod
    def actualizar_stock(cls, prod_id, cantidad_comprada):
        query = "UPDATE Productos SET stock = stock - ? WHERE id = ?"
        cls.db.execute_query(query, (cantidad_comprada, prod_id), commit=True)

    @classmethod
    def obtener_por_id(cls, prod_id):
        query = "SELECT * FROM Productos WHERE id = ?"
        return cls.db.fetch_one(query, (prod_id,))
