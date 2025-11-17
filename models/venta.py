from config.database import DatabaseManager
from models.producto import Producto


# Modelo para gestionar las ventas y sus detalles
class Venta:
    db = DatabaseManager()

    @classmethod
    def registrar_venta(cls, id_usuario, total, metodo_pago, detalles):
        conn = cls.db._get_connection()
        cursor = conn.cursor()

        try:
            # 1. Insertar en la tabla Ventas
            venta_query = (
                "INSERT INTO Ventas (id_usuario, total, metodo_pago) VALUES (?, ?, ?)"
            )
            cursor.execute(venta_query, (id_usuario, total, metodo_pago))
            id_venta = cursor.lastrowid

            # 2. Insertar en DetalleVentas y actualizar stock
            for item in detalles:
                detalle_query = "INSERT INTO DetalleVentas (id_venta, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)"
                cursor.execute(
                    detalle_query,
                    (id_venta, item["id_producto"], item["cantidad"], item["subtotal"]),
                )

                # Actualizar stock
                stock_query = "UPDATE Productos SET stock = stock - ? WHERE id = ?"
                cursor.execute(stock_query, (item["cantidad"], item["id_producto"]))

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"Error al registrar la venta: {e}")
            # Relanzar la excepción para que la GUI la maneje
            raise e
        finally:
            conn.close()
