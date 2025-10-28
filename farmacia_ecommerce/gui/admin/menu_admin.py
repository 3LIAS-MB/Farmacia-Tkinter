import tkinter as tk
from tkinter import ttk
from gui.admin.gestion_usuarios import GestionUsuarios
from gui.admin.gestion_productos import GestionProductos


class MenuAdmin:
    """Menú principal para el administrador."""

    def __init__(self, root, user_info):
        self.root = root
        self.user_info = user_info
        self.root.title(f"Menú Administrador - {self.user_info['username']}")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.center_window()

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(
            main_frame, text="Menú Principal", font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        # Botones del menú
        btn_style = ttk.Style()
        btn_style.configure("Admin.TButton", font=("Helvetica", 12), padding=10)

        btn_users = ttk.Button(
            main_frame,
            text="Gestión de Usuarios",
            style="Admin.TButton",
            command=self.open_gestion_usuarios,
        )
        btn_users.pack(pady=10, fill=tk.X)

        btn_products = ttk.Button(
            main_frame,
            text="Gestión de Productos",
            style="Admin.TButton",
            command=self.open_gestion_productos,
        )
        btn_products.pack(pady=10, fill=tk.X)

        btn_logout = ttk.Button(main_frame, text="Cerrar Sesión", command=self.logout)
        btn_logout.pack(pady=20)

    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def open_gestion_usuarios(self):
        """Abre la ventana de gestión de usuarios."""
        self.root.destroy()
        new_root = tk.Tk()
        GestionUsuarios(new_root, self.user_info)
        new_root.mainloop()

    def open_gestion_productos(self):
        """Abre la ventana de gestión de productos."""
        self.root.destroy()
        new_root = tk.Tk()
        GestionProductos(new_root, self.user_info)
        new_root.mainloop()

    def logout(self):
        """Cierra la sesión y vuelve a la pantalla de login."""
        self.root.destroy()
        from gui.login import LoginWindow

        new_root = tk.Tk()
        LoginWindow(new_root)
        new_root.mainloop()
