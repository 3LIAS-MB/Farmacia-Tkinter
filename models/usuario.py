import hashlib
from config.database import DatabaseManager


# Modelo para la gestión de usuarios en la base de datos
class Usuario:
    db = DatabaseManager()

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def autenticar(cls, username, password):
        hashed_password = cls._hash_password(password)
        query = "SELECT * FROM Usuarios WHERE username = ? AND password = ?"
        return cls.db.fetch_one(query, (username, hashed_password))

    @classmethod
    def crear(cls, username, password, rol):
        if cls.db.fetch_one("SELECT * FROM Usuarios WHERE username = ?", (username,)):
            print("Error: El nombre de usuario ya existe.")
            return False

        hashed_password = cls._hash_password(password)
        query = "INSERT INTO Usuarios (username, password, rol) VALUES (?, ?, ?)"
        cls.db.execute_query(query, (username, hashed_password, rol), commit=True)
        return True

    @classmethod
    def modificar(cls, user_id, username, rol):
        query = "UPDATE Usuarios SET username = ?, rol = ? WHERE id = ?"
        cls.db.execute_query(query, (username, rol, user_id), commit=True)

    @classmethod
    def eliminar(cls, user_id):
        query = "DELETE FROM Usuarios WHERE id = ?"
        cls.db.execute_query(query, (user_id,), commit=True)

    @classmethod
    def listar(cls):
        query = "SELECT id, username, rol FROM Usuarios"
        return cls.db.fetch_all(query)
