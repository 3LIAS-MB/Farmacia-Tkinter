import hashlib
from config.database import DatabaseManager

class Usuario:
    """Modelo para la gestión de usuarios en la base de datos."""

    db = DatabaseManager()

    @staticmethod
    def _hash_password(password):
        """Genera un hash SHA256 para la contraseña."""
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def autenticar(cls, username, password):
        """
        Autentica un usuario contra la base de datos.
        
        :param username: Nombre de usuario.
        :param password: Contraseña en texto plano.
        :return: Tupla con datos del usuario si es exitoso, None si no.
        """
        hashed_password = cls._hash_password(password)
        query = "SELECT * FROM Usuarios WHERE username = ? AND password = ?"
        return cls.db.fetch_one(query, (username, hashed_password))

    @classmethod
    def crear(cls, username, password, rol):
        """
        Crea un nuevo usuario.
        
        :param username: Nombre de usuario.
        :param password: Contraseña en texto plano.
        :param rol: Rol del usuario ('cliente' o 'admin').
        :return: True si se creó, False si hubo un error.
        """
        if cls.db.fetch_one("SELECT * FROM Usuarios WHERE username = ?", (username,)):
            print("Error: El nombre de usuario ya existe.")
            return False
        
        hashed_password = cls._hash_password(password)
        query = "INSERT INTO Usuarios (username, password, rol) VALUES (?, ?, ?)"
        cls.db.execute_query(query, (username, hashed_password, rol), commit=True)
        return True

    @classmethod
    def modificar(cls, user_id, username, rol):
        """
        Modifica los datos de un usuario existente.
        
        :param user_id: ID del usuario a modificar.
        :param username: Nuevo nombre de usuario.
        :param rol: Nuevo rol.
        """
        query = "UPDATE Usuarios SET username = ?, rol = ? WHERE id = ?"
        cls.db.execute_query(query, (username, rol, user_id), commit=True)

    @classmethod
    def eliminar(cls, user_id):
        """
        Elimina un usuario por su ID.
        
        :param user_id: ID del usuario a eliminar.
        """
        query = "DELETE FROM Usuarios WHERE id = ?"
        cls.db.execute_query(query, (user_id,), commit=True)  

    @classmethod
    def listar(cls):
        """ 
        Retorna una lista de todos los usuarios.
        
        :return: Lista de tuplas con (id, username, rol).
        """
        query = "SELECT id, username, rol FROM Usuarios"
        return cls.db.fetch_all(query)
