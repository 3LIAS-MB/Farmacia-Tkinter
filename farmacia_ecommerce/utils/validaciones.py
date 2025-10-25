from tkinter import messagebox

def validar_no_vacio(valor, nombre_campo):
    """
    Verifica que un campo no esté vacío.
    
    :param valor: El valor del campo a verificar.
    :param nombre_campo: El nombre del campo para mostrar en el mensaje de error.
    :return: True si es válido, False en caso contrario.
    """
    if not valor or not valor.strip():
        messagebox.showerror("Error de Validación", f"El campo '{nombre_campo}' no puede estar vacío.")
        return False
    return True

def validar_numero(valor, nombre_campo):
    """
    Verifica que un valor sea un número (entero).
    
    :param valor: El valor a verificar.
    :param nombre_campo: El nombre del campo para el mensaje de error.
    :return: True si es un número válido, False en caso contrario.
    """
    if not valor.isdigit():
        messagebox.showerror("Error de Validación", f"El campo '{nombre_campo}' debe ser un número entero.")
        return False
    return True

def validar_precio(valor, nombre_campo):
    """

    Verifica que un valor sea un número decimal (precio).
    
    :param valor: El valor a verificar.
    :param nombre_campo: El nombre del campo para el mensaje de error.
    :return: True si es un número válido, False en caso contrario.
    """
    try:
        float(valor)
        return True
    except ValueError:
        messagebox.showerror("Error de Validación", f"El campo '{nombre_campo}' debe ser un número válido (ej: 10.50).")
        return False
