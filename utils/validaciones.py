from tkinter import messagebox


def validar_no_vacio(valor, nombre_campo):
    if not valor or not valor.strip():
        messagebox.showerror(
            "Error de Validación", f"El campo '{nombre_campo}' no puede estar vacío."
        )
        return False
    return True


def validar_numero(valor, nombre_campo):
    if not valor.isdigit():
        messagebox.showerror(
            "Error de Validación",
            f"El campo '{nombre_campo}' debe ser un número entero.",
        )
        return False
    return True


def validar_precio(valor, nombre_campo):
    try:
        float(valor)
        return True
    except ValueError:
        messagebox.showerror(
            "Error de Validación",
            f"El campo '{nombre_campo}' debe ser un número válido (ej: 10.50).",
        )
        return False
