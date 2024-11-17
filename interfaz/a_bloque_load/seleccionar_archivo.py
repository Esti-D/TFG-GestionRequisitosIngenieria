import tkinter as tk
import os
import sys

from tkinter import filedialog
from almacenamiento.func_proyectos import obtener_proyectos

# Añade la carpeta raíz al sys.path para que Python pueda encontrar los módulos correctamente.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def seleccionar_archivo(entry_archivo, traducciones):
    """
    Abre el explorador de archivos para seleccionar un archivo PDF y actualiza el campo de entrada con la ruta seleccionada.

    Args:
        entry_archivo (tk.Entry): Campo de texto donde se mostrará la ruta del archivo seleccionado.
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.

    Flujo:
        1. Abre el explorador de archivos.
        2. Permite seleccionar solo archivos con extensión `.pdf`.
        3. Inserta la ruta del archivo seleccionado en el campo de entrada.

    """
    archivo = filedialog.askopenfilename(
        title=traducciones["M_Seleccionar_archivo_PDF"],
        filetypes=[("Archivos PDF", "*.pdf")],
    )
    if archivo:
        # Actualizar el campo de entrada con la ruta seleccionada.
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, archivo)


def ventana_seleccionar_proyecto(traducciones, callback):
    """
    Crea una ventana emergente para seleccionar un proyecto de una lista.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        callback (function): Función a la que se pasará el proyecto seleccionado.

    Flujo:
        1. Obtiene la lista de proyectos mediante `obtener_proyectos`.
        2. Muestra los proyectos en un Listbox.
        3. Permite seleccionar un proyecto y llama al callback con los datos.

    """
    # Crear ventana emergente.
    ventana = tk.Toplevel()
    ventana.title(traducciones["M_Seleccionar_proyecto"])
    ventana.geometry("400x300")

    # Obtener la lista de proyectos desde la base de datos.
    proyectos = obtener_proyectos()

    # Crear Listbox para mostrar los proyectos.
    lista_proyectos = tk.Listbox(ventana, height=10)
    for proyecto in proyectos:
        lista_proyectos.insert(tk.END, proyecto[1])  # Insertar nombre del proyecto.
    lista_proyectos.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Botón para aceptar la selección.
    boton_aceptar = tk.Button(
        ventana,
        text=traducciones["B_ACEPTAR"],
        command=lambda: callback(
            lista_proyectos.get(lista_proyectos.curselection()), proyectos, ventana
        ),
    )
    boton_aceptar.pack(pady=10, padx=20)


def aceptar_proyecto(
    proyecto_seleccionado, proyectos, ventana, entry_archivo, callback
):
    """
    Asocia el proyecto seleccionado al documento y cierra la ventana emergente.

    Args:
        proyecto_seleccionado (str): Nombre del proyecto seleccionado por el usuario.
        proyectos (list): Lista de proyectos disponibles, donde cada proyecto es una tupla (ID, nombre).
        ventana (tk.Toplevel): Ventana emergente que se cerrará tras la selección.
        entry_archivo (tk.Entry): Campo de texto donde se mostrará la ruta del archivo seleccionado.
        callback (function): Función que se ejecutará tras la selección del proyecto.

    Flujo:
        1. Busca el ID del proyecto seleccionado en la lista de proyectos.
        2. Cierra la ventana emergente.
        3. Llama al callback con el ID del proyecto.

    """
    # Buscar el ID del proyecto seleccionado.
    for proyecto in proyectos:
        if proyecto[1] == proyecto_seleccionado:
            proyecto_id = proyecto[0]
            break
    ventana.destroy()  # Cerrar la ventana emergente.
    callback(proyecto_id)  # Llamar al callback con el ID del proyecto.
