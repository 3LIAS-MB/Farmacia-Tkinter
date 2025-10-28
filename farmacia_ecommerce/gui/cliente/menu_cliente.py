import tkinter as tk
from tkinter import ttk
from gui.cliente.consulta_productos import ConsultaProductos
from gui.cliente.proceso_compra import ProcesoCompra


class MenuCliente:
    """Menú principal para el cliente."""

    def __init__(self, root, user_info):
        self.root = root
        self.user_info = user_info
        self.root.title(f"Menú Cliente - {self.user_info['username']}")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.center_window()

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(
            main_frame, text="Bienvenido a la Farmacia", font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        btn_style = ttk.Style()
        btn_style.configure("Client.TButton", font=("Helvetica", 12), padding=10)

        btn_consult = ttk.Button(
            main_frame,
            text="Consultar Productos",
            style="Client.TButton",
            command=self.open_consulta_productos,
        )
        btn_consult.pack(pady=10, fill=tk.X)

        btn_buy = ttk.Button(
            main_frame,
            text="Realizar Compra",
            style="Client.TButton",
            command=self.open_proceso_compra,
        )
        btn_buy.pack(pady=10, fill=tk.X)

        btn_logout = ttk.Button(main_frame, text="Cerrar Sesión", command=self.logout)
        btn_logout.pack(pady=20)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def open_consulta_productos(self):
        self.root.destroy()
        new_root = tk.Tk()
        ConsultaProductos(new_root, self.user_info)
        new_root.mainloop()

    def open_proceso_compra(self):
        self.root.destroy()
        new_root = tk.Tk()
        ProcesoCompra(new_root, self.user_info)
        new_root.mainloop()

    def logout(self):
        self.root.destroy()
        from gui.login import LoginWindow

        new_root = tk.Tk()
        LoginWindow(new_root)
        new_root.mainloop()
