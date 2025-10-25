import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.producto import Producto
from models.venta import Venta # Necesitaremos crear este modelo

class ProcesoCompra:
    """Ventana para el proceso de compra y gestión del carrito."""

    def __init__(self, root, user_info):
        self.root = root
        self.user_info = user_info
        self.root.title("Proceso de Compra")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        self.center_window()

        self.carrito = {} # {id_producto: (nombre, cantidad, precio, subtotal)}

        # --- Layout Principal ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # --- Panel Izquierdo (Productos Disponibles) ---
        products_frame = ttk.LabelFrame(main_frame, text="Productos Disponibles", padding="10")
        products_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        products_frame.grid_rowconfigure(1, weight=1)
        products_frame.grid_columnconfigure(0, weight=1)

        # Búsqueda de productos
        search_bar = ttk.Entry(products_frame)
        search_bar.grid(row=0, column=0, sticky="ew", pady=5)
        search_bar.bind("<KeyRelease>", self._on_search)

        # Treeview de productos
        self.products_tree = ttk.Treeview(products_frame, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Nombre", text="Nombre")
        self.products_tree.heading("Precio", text="Precio")
        self.products_tree.heading("Stock", text="Stock")
        self.products_tree.column("ID", width=40)
        self.products_tree.column("Precio", width=60, anchor="e")
        self.products_tree.column("Stock", width=60, anchor="center")
        self.products_tree.grid(row=1, column=0, sticky="nsew")
        self._cargar_productos()

        ttk.Button(products_frame, text="Agregar al Carrito", command=self._agregar_al_carrito).grid(row=2, column=0, pady=10)

        # --- Panel Derecho (Carrito y Finalización) ---
        cart_frame = ttk.LabelFrame(main_frame, text="Carrito de Compras", padding="10")
        cart_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        cart_frame.grid_rowconfigure(0, weight=1)
        cart_frame.grid_columnconfigure(0, weight=1)

        # Treeview del carrito
        self.cart_tree = ttk.Treeview(cart_frame, columns=("Nombre", "Cantidad", "Precio", "Subtotal"), show="headings")
        self.cart_tree.heading("Nombre", text="Nombre")
        self.cart_tree.heading("Cantidad", text="Cantidad")
        self.cart_tree.heading("Precio", text="Precio Unit.")
        self.cart_tree.heading("Subtotal", text="Subtotal")
        self.cart_tree.column("Cantidad", width=80, anchor="center")
        self.cart_tree.column("Precio", width=100, anchor="e")
        self.cart_tree.column("Subtotal", width=100, anchor="e")
        self.cart_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Botones del carrito
        cart_btn_frame = ttk.Frame(cart_frame)
        cart_btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(cart_btn_frame, text="Eliminar Producto", command=self._eliminar_del_carrito).pack(side="left", padx=5)
        ttk.Button(cart_btn_frame, text="Vaciar Carrito", command=self._vaciar_carrito).pack(side="left", padx=5)

        # Total y Pago
        summary_frame = ttk.Frame(cart_frame)
        summary_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        self.total_label = ttk.Label(summary_frame, text="Total: 0.00 €", font=("Helvetica", 14, "bold"))
        self.total_label.pack(side="left", padx=10)
        
        payment_frame = ttk.LabelFrame(cart_frame, text="Método de Pago", padding="10")
        payment_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.metodo_pago = tk.StringVar(value="Contado")
        ttk.Radiobutton(payment_frame, text="Contado", variable=self.metodo_pago, value="Contado").pack(side="left", padx=10)
        ttk.Radiobutton(payment_frame, text="Tarjeta de Débito", variable=self.metodo_pago, value="Tarjeta de Débito").pack(side="left", padx=10)
        ttk.Radiobutton(payment_frame, text="Tarjeta de Crédito", variable=self.metodo_pago, value="Tarjeta de Crédito").pack(side="left", padx=10)

        # Botón Finalizar
        ttk.Button(cart_frame, text="Finalizar Compra", style="Accent.TButton", command=self._finalizar_compra).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Style().configure("Accent.TButton", font=("Helvetica", 12, "bold"), padding=10)

        # Botón Volver
        ttk.Button(main_frame, text="Volver al Menú", command=self._volver).grid(row=1, column=0, columnspan=2, pady=10)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _cargar_productos(self, search_term=""):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        productos = Producto.listar()
        for prod in productos:
            if search_term.lower() in prod[1].lower():
                self.products_tree.insert("", tk.END, values=(prod[0], prod[1], f"{prod[3]:.2f}", prod[4]), iid=prod[0])

    def _on_search(self, event):
        self._cargar_productos(event.widget.get())

    def _agregar_al_carrito(self):
        selected_items = self.products_tree.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "Seleccione un producto para agregar.")
            return
        
        prod_id = int(selected_items[0])
        producto = Producto.obtener_por_id(prod_id)
        
        if producto[4] <= 0: # Stock
            messagebox.showerror("Error", "Producto sin stock.")
            return

        cantidad = simpledialog.askinteger("Cantidad", f"¿Cuántas unidades de '{producto[1]}' desea?", parent=self.root, minvalue=1, maxvalue=producto[4])
        
        if cantidad:
            if prod_id in self.carrito:
                self.carrito[prod_id] = (
                    producto[1],
                    self.carrito[prod_id][1] + cantidad,
                    producto[3],
                    (self.carrito[prod_id][1] + cantidad) * producto[3]
                )
            else:
                self.carrito[prod_id] = (producto[1], cantidad, producto[3], cantidad * producto[3])
            
            self._actualizar_carrito_treeview()

    def _actualizar_carrito_treeview(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        total = 0
        for prod_id, data in self.carrito.items():
            nombre, cantidad, precio, subtotal = data
            self.cart_tree.insert("", tk.END, values=(nombre, cantidad, f"{precio:.2f}", f"{subtotal:.2f}"), iid=prod_id)
            total += subtotal
        
        self.total_label.config(text=f"Total: {total:.2f} €")

    def _eliminar_del_carrito(self):
        selected_items = self.cart_tree.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "Seleccione un producto del carrito para eliminar.")
            return
        
        prod_id = int(selected_items[0])
        del self.carrito[prod_id]
        self._actualizar_carrito_treeview()

    def _vaciar_carrito(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea vaciar el carrito?"):
            self.carrito.clear()
            self._actualizar_carrito_treeview()

    def _finalizar_compra(self):
        if not self.carrito:
            messagebox.showerror("Error", "El carrito está vacío.")
            return

        total = sum(data[3] for data in self.carrito.values())
        metodo_pago = self.metodo_pago.get()
        id_usuario = self.user_info['id']
        
        # Detalles de la venta para el modelo
        detalles = []
        for prod_id, data in self.carrito.items():
            detalles.append({
                'id_producto': prod_id,
                'cantidad': data[1],
                'subtotal': data[3]
            })

        try:
            Venta.registrar_venta(id_usuario, total, metodo_pago, detalles)
            messagebox.showinfo("Éxito", "Compra realizada con éxito.")
            self.carrito.clear()
            self._actualizar_carrito_treeview()
            self._cargar_productos() # Recargar para ver stock actualizado
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la compra: {e}")

    def _volver(self):
        self.root.destroy()
        from gui.cliente.menu_cliente import MenuCliente
        new_root = tk.Tk()
        MenuCliente(new_root, self.user_info)
        new_root.mainloop()
