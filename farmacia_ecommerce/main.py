import tkinter as tk
from tkinter import ttk

from config.database import DatabaseManager
from gui.login import LoginWindow


def setup_styles():
    """Configura estilos globales para la aplicación ttk."""
    style = ttk.Style()
    style.theme_use("clam")

    # Estilo para botones
    style.configure(
        "TButton",
        font=("Helvetica", 10),
        padding=5,
        background="#e0e0e0",
        borderwidth=1,
        relief="raised",
    )
    style.map("TButton", background=[("active", "#c0c0c0")])

    # Estilo para Labels
    style.configure("TLabel", font=("Helvetica", 11), padding=5)

    # Estilo para Frames
    style.configure("TFrame", background="#f0f0f0")

    # Estilo para Treeview
    style.configure("Treeview", rowheight=25, font=("Helvetica", 10))
    style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))

    # Estilo para LabelFrames
    style.configure("TLabelframe", padding=10, font=("Helvetica", 12, "italic"))
    style.configure(
        "TLabelframe.Label", font=("Helvetica", 12, "bold"), foreground="navy"
    )


def main():
    # 1. Inicializar la base de datos
    print("Inicializando la base de datos...")
    db_manager = DatabaseManager(db_path="farmacia.db")
    db_manager.init_db()
    print("Base de datos lista.")

    # 2. Crear la ventana principal y la aplicación de login
    root = tk.Tk()
    setup_styles()

    # La ventana de login se encargará de mostrarse y gestionar el flujo
    app = LoginWindow(root)

    # 3. Iniciar el bucle de eventos de la GUI
    root.mainloop()


if __name__ == "__main__":
    main()
