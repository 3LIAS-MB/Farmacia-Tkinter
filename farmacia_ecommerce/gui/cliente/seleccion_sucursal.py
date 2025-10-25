import tkinter as tk
from tkinter import ttk, messagebox
from models.sucursal import Sucursal

class SeleccionSucursal:
    """
    Ventana para seleccionar una sucursal.
    Esta clase puede ser instanciada y mostrada como un diálogo modal.
    """
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Seleccionar Sucursal")
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent) # Mantener por encima de la ventana padre
        self.dialog.grab_set() # Modal

        self.selected_sucursal = None

        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Seleccione una sucursal para la entrega:", font=('Helvetica', 12)).pack(pady=5)

        # --- Treeview para sucursales ---
        self.tree = ttk.Treeview(main_frame, columns=("Nombre", "Dirección", "Distancia"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Distancia", text="Distancia (km)")
        
        self.tree.column("Nombre", width=150)
        self.tree.column("Dirección", width=200)
        self.tree.column("Distancia", width=100, anchor=tk.E)

        self.tree.pack(expand=True, fill=tk.BOTH, pady=10)
        self._cargar_sucursales()

        # --- Botones ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Confirmar Selección", command=self._confirmar).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Seleccionar Más Cercana", command=self._seleccionar_cercana).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=self._cancelar).pack(side=tk.LEFT, padx=10)

        self.center_window()

    def center_window(self):
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        parent_x = self.dialog.master.winfo_x()
        parent_y = self.dialog.master.winfo_y()
        parent_width = self.dialog.master.winfo_width()
        parent_height = self.dialog.master.winfo_height()
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')

    def _cargar_sucursales(self):
        sucursales = Sucursal.listar()
        for suc in sucursales:
            # id, nombre, direccion, distancia
            self.tree.insert("", tk.END, values=(suc[1], suc[2], f"{suc[3]:.2f} km"), iid=suc[0])

    def _confirmar(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "Debe seleccionar una sucursal.", parent=self.dialog)
            return
        
        item_id = selected_items[0]
        item = self.tree.item(item_id)
        self.selected_sucursal = (item_id, item['values'][0]) # (id, nombre)
        self.dialog.destroy()

    def _seleccionar_cercana(self):
        sucursal = Sucursal.obtener_mas_cercana()
        if sucursal:
            self.selected_sucursal = (sucursal[0], sucursal[1]) # (id, nombre)
            messagebox.showinfo("Info", f"Se ha seleccionado la sucursal más cercana: {sucursal[1]}", parent=self.dialog)
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "No se encontraron sucursales.", parent=self.dialog)

    def _cancelar(self):
        self.selected_sucursal = None
        self.dialog.destroy()

    def show(self):
        """Muestra el diálogo y espera hasta que se cierre."""
        self.dialog.wait_window()
        return self.selected_sucursal
