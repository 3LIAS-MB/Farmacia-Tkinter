import tkinter as tk
from tkinter import ttk, messagebox
from models.producto import Producto


class ConsultaProductos:
    """Ventana para que el cliente consulte productos."""

    def __init__(self, root, user_info):
        self.root = root
        self.user_info = user_info
        self.root.title("Consulta de Productos")
        self.root.geometry("800x500")
        self.root.minsize(600, 400)
        self.center_window()

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Búsqueda ---
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Buscar por nombre:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.search_entry.bind(
            "<KeyRelease>", self._on_search
        )  # Evento al soltar una tecla

        # --- Tabla ---
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Nombre", "Descripción", "Precio", "Stock"),
            show="headings",
        )
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Precio", text="Precio (€)")
        self.tree.heading("Stock", text="Stock Disponible")

        self.tree.column("Nombre", width=200)
        self.tree.column("Descripción", width=300)
        self.tree.column("Precio", width=80, anchor=tk.E)
        self.tree.column("Stock", width=100, anchor=tk.CENTER)

        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(main_frame, text="Volver al Menú", command=self._volver).pack(
            pady=10
        )

        self._cargar_productos()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _cargar_productos(self, search_term=""):
        """Carga productos en la tabla, opcionalmente filtrados por un término de búsqueda."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        productos = Producto.consultar(search_term)

        if not productos:
            # Insertar un mensaje en la tabla si no hay resultados
            self.tree.insert(
                "",
                tk.END,
                values=("No se encontraron productos", "", "", ""),
                tags=("empty",),
            )
            self.tree.tag_configure("empty", foreground="grey")
            return

        for prod in productos:
            nombre, desc, precio, stock = prod
            stock_disponible = "Sí" if stock > 0 else "No"
            formatted_precio = f"{precio:.2f}"
            self.tree.insert(
                "", tk.END, values=(nombre, desc, formatted_precio, stock_disponible)
            )

    def _on_search(self, event):
        """Se ejecuta cada vez que el usuario escribe en el campo de búsqueda."""
        search_term = self.search_entry.get()
        self._cargar_productos(search_term)

    def _volver(self):
        self.root.destroy()
        from gui.cliente.menu_cliente import MenuCliente

        new_root = tk.Tk()
        MenuCliente(new_root, self.user_info)
        new_root.mainloop()
