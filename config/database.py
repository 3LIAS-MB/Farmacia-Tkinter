import sqlite3
import hashlib


class DatabaseManager:
    # Gestiona la conexión y las operaciones con la base de datos SQLite. (constructor)
    def __init__(self, db_path="farmacia.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=(), commit=False):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                if commit:
                    conn.commit()
                return cursor
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
            return None

    def fetch_all(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall() if cursor else []

    def fetch_one(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchone() if cursor else None

    def _create_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('cliente', 'admin'))
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Sucursales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                distancia_km REAL NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total REAL NOT NULL,
                metodo_pago TEXT,
                FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS DetalleVentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER,
                id_producto INTEGER,
                cantidad INTEGER NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (id_venta) REFERENCES Ventas(id),
                FOREIGN KEY (id_producto) REFERENCES Productos(id)
            );
            """,
        ]
        for query in queries:
            self.execute_query(query, commit=True)
        print("Tablas creadas o ya existentes.")

    def _insert_initial_data(self):
        def hash_password(password):
            return hashlib.sha256(password.encode()).hexdigest()

        # Usuarios (admin/admin123, cliente/cliente123)
        initial_users = [
            ("admin", hash_password("admin123"), "admin"),
            ("cliente", hash_password("cliente123"), "cliente"),
        ]
        for user in initial_users:
            self.execute_query(
                "INSERT OR IGNORE INTO Usuarios (username, password, rol) VALUES (?, ?, ?)",
                user,
                commit=True,
            )

        # Productos
        initial_products = [
            ("Ibuprofeno 400mg", "Analgésico y antiinflamatorio", 5.50, 100),
            ("Paracetamol 500mg", "Analgésico y antipirético", 3.75, 150),
            ("Amoxicilina 500mg", "Antibiótico de amplio espectro", 12.00, 80),
        ]
        for prod in initial_products:
            self.execute_query(
                "INSERT OR IGNORE INTO Productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)",
                prod,
                commit=True,
            )

        # Sucursales
        initial_sucursales = [
            ("Sucursal Centro", "Av. Principal 123", 2.5),
            ("Sucursal Norte", "Calle 45 #678", 5.8),
        ]
        for suc in initial_sucursales:
            self.execute_query(
                "INSERT OR IGNORE INTO Sucursales (nombre, direccion, distancia_km) VALUES (?, ?, ?)",
                suc,
                commit=True,
            )
        print("Datos iniciales insertados.")

    def init_db(self):
        self._create_tables()
        self._insert_initial_data()


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.init_db()
    print("Base de datos inicializada correctamente.")
