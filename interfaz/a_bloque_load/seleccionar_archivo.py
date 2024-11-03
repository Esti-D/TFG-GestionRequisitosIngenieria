import tkinter as tk
import os
import sys

from tkinter import filedialog
from almacenamiento.func_proyectos import obtener_proyectos

# Añade la carpeta raíz al sys.path para que Python pueda encontrar los módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def seleccionar_archivo(entry_archivo, traducciones):
    """Abre el explorador de archivos para seleccionar un archivo PDF."""
    archivo = filedialog.askopenfilename(
        title=traducciones["M_Seleccionar_archivo_PDF"],
        filetypes=[("Archivos PDF", "*.pdf")],
    )
    if archivo:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, archivo)


def ventana_seleccionar_proyecto(traducciones, callback):
    """Crea una ventana para seleccionar un proyecto de una lista."""
    ventana = tk.Toplevel()
    ventana.title(traducciones["M_Seleccionar_proyecto"])
    ventana.geometry("400x300")

    proyectos = obtener_proyectos()

    lista_proyectos = tk.Listbox(ventana, height=10)
    for proyecto in proyectos:
        lista_proyectos.insert(tk.END, proyecto[1])
    lista_proyectos.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

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
    """Asocia el proyecto seleccionado al documento y cierra la ventana."""
    for proyecto in proyectos:
        if proyecto[1] == proyecto_seleccionado:
            proyecto_id = proyecto[0]
            break
    ventana.destroy()  # Cerrar la ventana
    callback(proyecto_id)  # Llamar al callback con el ID del proyecto
