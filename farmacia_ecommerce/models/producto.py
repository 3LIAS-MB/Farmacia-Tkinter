from config.database import DatabaseManager

class Producto:
    """Modelo para la gestión de productos en la base de datos."""

    db = DatabaseManager()

    @classmethod
    def consultar(cls, nombre):
        """
        Busca productos por nombre.
        
        :param nombre: Nombre o parte del nombre del producto a buscar.
        :return: Lista de productos que coinciden con la búsqueda.
        """
        query = "SELECT nombre, descripcion, precio, stock FROM Productos WHERE nombre LIKE ?"
        return cls.db.fetch_all(query, (f'%{nombre}%',))

    @classmethod
    def crear(cls, nombre, descripcion, precio, stock):
        """
        Crea un nuevo producto.
        
        :param nombre: Nombre del producto.
        :param descripcion: Descripción del producto.
        :param precio: Precio del producto.
        :param stock: Stock inicial del producto.
        """
        query = "INSERT INTO Productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)"
        cls.db.execute_query(query, (nombre, descripcion, precio, stock), commit=True)

    @classmethod
    def modificar(cls, prod_id, nombre, descripcion, precio, stock):
        """
        Modifica un producto existente.
        
        :param prod_id: ID del producto a modificar.
        :param nombre: Nuevo nombre.
        :param descripcion: Nueva descripción.
        :param precio: Nuevo precio.
        :param stock: Nuevo stock.
        """
        query = "UPDATE Productos SET nombre = ?, descripcion = ?, precio = ?, stock = ? WHERE id = ?"
        cls.db.execute_query(query, (nombre, descripcion, precio, stock, prod_id), commit=True)

    @classmethod
    def eliminar(cls, prod_id):
        """
        Elimina un producto por su ID.
        
        :param prod_id: ID del producto a eliminar.
        """
        query = "DELETE FROM Productos WHERE id = ?"
        cls.db.execute_query(query, (prod_id,), commit=True)

    @classmethod
    def listar(cls):
        """
        Retorna una lista de todos los productos.
        
        :return: Lista de tuplas con (id, nombre, descripcion, precio, stock).
        """
        query = "SELECT * FROM Productos"
        return cls.db.fetch_all(query)

    @classmethod
    def actualizar_stock(cls, prod_id, cantidad_comprada):
        """
        Actualiza el stock de un producto después de una venta.
        
        :param prod_id: ID del producto.
        :param cantidad_comprada: Cantidad de unidades vendidas.
        """
        query = "UPDATE Productos SET stock = stock - ? WHERE id = ?"
        cls.db.execute_query(query, (cantidad_comprada, prod_id), commit=True)

    @classmethod
    def obtener_por_id(cls, prod_id):
        """
        Obtiene un producto por su ID.
        
        :param prod_id: ID del producto.
        :return: Tupla con los datos del producto.
        """
        query = "SELECT * FROM Productos WHERE id = ?"
        return cls.db.fetch_one(query, (prod_id,))
