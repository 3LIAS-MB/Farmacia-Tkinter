import tkinter as tk
from tkinter import ttk, messagebox
from models.producto import Producto
from utils.validaciones import validar_no_vacio, validar_precio, validar_numero

class GestionProductos:
    """Ventana para la gestión CRUD de productos."""

    def __init__(self, root, user_info):
        self.root = root
        self.user_info = user_info
        self.root.title("Gestión de Productos")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)
        self.center_window()

        # --- Layout ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        form_frame = ttk.LabelFrame(main_frame, text="Datos del Producto", padding="10")
        form_frame.pack(fill=tk.X, pady=5)

        table_frame = ttk.Frame(main_frame)
        table_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        # --- Formulario ---
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.nombre_entry = ttk.Entry(form_frame, width=40)
        self.nombre_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)

        ttk.Label(form_frame, text="Precio:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.precio_entry = ttk.Entry(form_frame, width=15)
        self.precio_entry.grid(row=0, column=3, sticky=tk.W, padx=5)

        ttk.Label(form_frame, text="Stock:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.stock_entry = ttk.Entry(form_frame, width=15)
        self.stock_entry.grid(row=0, column=5, sticky=tk.W, padx=5)

        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1, columnspan=5, sticky=tk.EW, padx=5, pady=5)
        
        form_frame.grid_columnconfigure(1, weight=1)

        # --- Botones del Formulario ---
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=6, pady=10)
        
        ttk.Button(btn_frame, text="Crear", command=self._crear).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Modificar", command=self._modificar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self._eliminar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self._limpiar).pack(side=tk.LEFT, padx=5)

        # --- Tabla (Treeview) ---
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Descripción", "Precio", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Precio", text="Precio (€)")
        self.tree.heading("Stock", text="Stock (uds.)")

        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Nombre", width=200)
        self.tree.column("Descripción", width=300)
        self.tree.column("Precio", width=80, anchor=tk.E)
        self.tree.column("Stock", width=80, anchor=tk.CENTER)

        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_item_select)

        ttk.Button(main_frame, text="Volver al Menú", command=self._volver).pack(pady=10)

        self.selected_prod_id = None
        self._cargar_productos()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _cargar_productos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = Producto.listar()
        for prod in productos:
            # Formatear precio a 2 decimales
            formatted_prod = list(prod)
            formatted_prod[3] = f"{prod[3]:.2f}"
            self.tree.insert("", tk.END, values=formatted_prod)

    def _on_item_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        item = self.tree.item(selected_items[0])
        prod_id, nombre, desc, precio, stock = item['values']

        self.selected_prod_id = prod_id
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, nombre)
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, desc)
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, precio)
        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, stock)

    def _limpiar(self):
        self.selected_prod_id = None
        self.nombre_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def _crear(self):
        nombre = self.nombre_entry.get()
        desc = self.desc_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()

        if not all([
            validar_no_vacio(nombre, "Nombre"),
            validar_precio(precio, "Precio"),
            validar_numero(stock, "Stock")
        ]):
            return

        Producto.crear(nombre, desc, float(precio), int(stock))
        messagebox.showinfo("Éxito", "Producto creado correctamente.")
        self._cargar_productos()
        self._limpiar()

    def _modificar(self):
        if self.selected_prod_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un producto para modificar.")
            return

        nombre = self.nombre_entry.get()
        desc = self.desc_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()

        if not all([
            validar_no_vacio(nombre, "Nombre"),
            validar_precio(precio, "Precio"),
            validar_numero(stock, "Stock")
        ]):
            return

        Producto.modificar(self.selected_prod_id, nombre, desc, float(precio), int(stock))
        messagebox.showinfo("Éxito", "Producto modificado correctamente.")
        self._cargar_productos()
        self._limpiar()

    def _eliminar(self):
        if self.selected_prod_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este producto?"):
            Producto.eliminar(self.selected_prod_id)
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            self._cargar_productos()
            self._limpiar()

    def _volver(self):
        self.root.destroy()
        from gui.admin.menu_admin import MenuAdmin
        new_root = tk.Tk()
        MenuAdmin(new_root, self.user_info)
        new_root.mainloop()
