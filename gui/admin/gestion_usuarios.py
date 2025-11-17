import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario
from utils.validaciones import validar_no_vacio


class GestionUsuarios:
    # Ventana para la gestión CRUD de usuarios.
    def __init__(self, root, user_info):
        self.root = root
        self.user_info = user_info
        self.root.title("Gestión de Usuarios")
        self.root.geometry("800x500")
        self.root.minsize(600, 400)
        self.center_window()

        # --- Layout ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para el formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Usuario", padding="10")
        form_frame.pack(fill=tk.X, pady=5)

        # Frame para la tabla y botones
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        # --- Formulario ---
        ttk.Label(form_frame, text="Username:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)

        ttk.Label(form_frame, text="Password:").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5
        )
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=0, column=3, sticky=tk.EW, padx=5)
        ttk.Label(form_frame, text="(Dejar en blanco para no cambiar)").grid(
            row=1, column=3, sticky=tk.W, padx=5
        )

        ttk.Label(form_frame, text="Rol:").grid(
            row=0, column=4, sticky=tk.W, padx=5, pady=5
        )
        self.rol_combobox = ttk.Combobox(
            form_frame, values=["cliente", "admin"], state="readonly"
        )
        self.rol_combobox.grid(row=0, column=5, sticky=tk.EW, padx=5)
        self.rol_combobox.set("cliente")

        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
        form_frame.grid_columnconfigure(5, weight=1)

        # --- Botones del Formulario ---
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=6, pady=10)

        ttk.Button(btn_frame, text="Crear", command=self._crear_usuario).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Modificar", command=self._modificar_usuario).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Eliminar", command=self._eliminar_usuario).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Limpiar", command=self._limpiar_formulario).pack(
            side=tk.LEFT, padx=5
        )

        # --- Tabla (Treeview) ---
        self.tree = ttk.Treeview(
            table_frame, columns=("ID", "Username", "Rol"), show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Username", text="Nombre de Usuario")
        self.tree.heading("Rol", text="Rol")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Username", width=200)
        self.tree.column("Rol", width=100, anchor=tk.CENTER)

        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_item_select)

        # Botón para volver
        ttk.Button(main_frame, text="Volver al Menú", command=self._volver).pack(
            pady=10
        )

        self.selected_user_id = None
        self._cargar_usuarios()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _cargar_usuarios(self):
        """Carga o recarga los usuarios en el Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        usuarios = Usuario.listar()
        for user in usuarios:
            self.tree.insert("", tk.END, values=user)

    def _on_item_select(self, event):
        """Maneja la selección de un item en la tabla."""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = self.tree.item(selected_items[0])
        user_id, username, rol = item["values"]

        self.selected_user_id = user_id
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)
        self.rol_combobox.set(rol)
        self.password_entry.delete(0, tk.END)

    def _limpiar_formulario(self):
        """Limpia los campos del formulario."""
        self.selected_user_id = None
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.rol_combobox.set("cliente")
        self.tree.selection_remove(self.tree.selection())

    def _crear_usuario(self):
        """Crea un nuevo usuario."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        rol = self.rol_combobox.get()

        if not all(
            [
                validar_no_vacio(username, "Username"),
                validar_no_vacio(password, "Password"),
            ]
        ):
            return

        if Usuario.crear(username, password, rol):
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            self._cargar_usuarios()
            self._limpiar_formulario()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")

    def _modificar_usuario(self):
        """Modifica un usuario existente."""
        if self.selected_user_id is None:
            messagebox.showwarning(
                "Advertencia", "Seleccione un usuario para modificar."
            )
            return

        username = self.username_entry.get()
        rol = self.rol_combobox.get()
        password = self.password_entry.get()

        if not validar_no_vacio(username, "Username"):
            return

        # Lógica para no cambiar la contraseña si el campo está vacío
        if password:
            # Aquí se debería llamar a un método para cambiar también la contraseña
            # Por simplicidad, este ejemplo solo actualiza username y rol.
            # Para una app real, se necesitaría un Usuario.modificar_con_pass()
            messagebox.showwarning(
                "Info",
                "La modificación de contraseña no está implementada en este formulario. Solo se actualizarán el username y el rol.",
            )

        Usuario.modificar(self.selected_user_id, username, rol)
        messagebox.showinfo("Éxito", "Usuario modificado correctamente.")
        self._cargar_usuarios()
        self._limpiar_formulario()

    def _eliminar_usuario(self):
        """Elimina un usuario seleccionado."""
        if self.selected_user_id is None:
            messagebox.showwarning(
                "Advertencia", "Seleccione un usuario para eliminar."
            )
            return

        if self.selected_user_id == self.user_info["id"]:
            messagebox.showerror("Error", "No puede eliminar a su propio usuario.")
            return

        if messagebox.askyesno(
            "Confirmar", "¿Está seguro de que desea eliminar este usuario?"
        ):
            Usuario.eliminar(self.selected_user_id)
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            self._cargar_usuarios()
            self._limpiar_formulario()

    def _volver(self):
        """Vuelve al menú principal del administrador."""
        self.root.destroy()
        from gui.admin.menu_admin import MenuAdmin

        new_root = tk.Tk()
        MenuAdmin(new_root, self.user_info)
        new_root.mainloop()
