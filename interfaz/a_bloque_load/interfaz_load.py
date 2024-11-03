import tkinter as tk
from tkinter import filedialog
import os
import sys

from .seleccionar_archivo import (
    seleccionar_archivo,
    ventana_seleccionar_proyecto,
    aceptar_proyecto,
)
from .cargar_documento import cargar_documento, guardar_requisitos_y_asociaciones
from .asignar_subsistemas import (
    asignar_subsistemas_a_documento_y_mostrar_ventana,
    aceptar_asignacion_subsistemas,
)


def crear_bloque_load(frame_funcionalidades, traducciones, frame_visual):
    """Crea el bloque de carga de archivos y proyectos"""
    # Crear el frame de LOAD dentro del frame de funcionalidades
    frame_load = tk.Frame(
        frame_funcionalidades,
        bg="#125ca6",
        highlightbackground="#3790e9",
        highlightthickness=3,
        padx=5,
        pady=3,
    )
    frame_load.grid(row=0, column=0, padx=10, pady=8, sticky="ew")

    # Configurar la columna del frame_load para que se expanda
    frame_load.grid_columnconfigure(0, weight=1)

    # Cuadro de texto para mostrar la ruta del archivo seleccionado
    entry_archivo = tk.Entry(frame_load)
    entry_archivo.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    # Botón de LOAD
    boton_load = tk.Button(
        frame_load,
        text=traducciones["P_LOAD"],
        command=lambda: ventana_seleccionar_proyecto(
            traducciones,
            lambda proyecto_nombre, proyectos, ventana: aceptar_proyecto(
                proyecto_nombre,
                proyectos,
                ventana,
                entry_archivo,
                lambda proyecto_id: cargar_documento(
                    traducciones, entry_archivo, proyecto_id, frame_visual
                ),
            ),
        ),
    )
    boton_load.grid(row=0, column=0, padx=10, pady=8, sticky="ew", ipady=8)

    # Botón de Seleccionar archivo
    boton_seleccionar = tk.Button(
        frame_load,
        text=traducciones["P_SELECCIONAR"],
        command=lambda: seleccionar_archivo(entry_archivo, traducciones),
    )
    boton_seleccionar.grid(row=1, column=0, padx=10, pady=8, sticky="ew")

    return frame_load
