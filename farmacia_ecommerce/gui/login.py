import tkinter as tk
from tkinter import ttk, messagebox

from models.usuario import Usuario
from gui.admin.menu_admin import MenuAdmin
from gui.cliente.menu_cliente import MenuCliente


class LoginWindow:
    """Ventana de inicio de sesión."""

    def __init__(self, root):
        self.root = root
        self.root.title("Farmacia E-commerce - Login")
        self.root.geometry("350x200")
        self.root.resizable(False, False)
        self.center_window()

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.user_info = None

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Widgets
        ttk.Label(main_frame, text="Usuario:", font=("Helvetica", 12)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.username_entry = ttk.Entry(main_frame, width=25)
        self.username_entry.grid(row=0, column=1, sticky=tk.EW)

        ttk.Label(main_frame, text="Contraseña:", font=("Helvetica", 12)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.password_entry = ttk.Entry(main_frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1, sticky=tk.EW)

        login_button = ttk.Button(
            main_frame, text="Iniciar Sesión", command=self._handle_login
        )
        login_button.grid(row=2, column=0, columnspan=2, pady=15)

        # Centrar widgets
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _handle_login(self):
        """Gestiona el evento de clic en el botón de login."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña son requeridos.")
            return

        user_data = Usuario.autenticar(username, password)

        if user_data:
            self.user_info = {
                "id": user_data[0],
                "username": user_data[1],
                "rol": user_data[3],
            }
            messagebox.showinfo("Éxito", f"Bienvenido {self.user_info['username']}")
            self.root.destroy()  # Cierra la ventana de login
            self._redirect()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def _redirect(self):
        """Redirige al menú correspondiente según el rol del usuario."""
        new_root = tk.Tk()
        if self.user_info["rol"] == "admin":
            MenuAdmin(new_root, self.user_info)
        else:
            MenuCliente(new_root, self.user_info)
        new_root.mainloop()
