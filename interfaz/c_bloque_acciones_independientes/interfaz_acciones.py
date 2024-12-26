"""
Archivo: bloque_acciones.py
Descripción: Este archivo define el bloque "Acciones" de la interfaz gráfica, que incluye botones
para gestionar proyectos, subsistemas y asignaciones.

Autor: Estíbalitz Díez
Fecha: 26/12/2024
Versión: 2
"""

import tkinter as tk
from interfaz.c_bloque_acciones_independientes.bloque_asignaciones import (
    crear_boton_asignar,
)
from interfaz.c_bloque_acciones_independientes.bloque_proyectos import (
    crear_boton_proyecto,
)
from interfaz.c_bloque_acciones_independientes.bloque_subsistemas import (
    crear_boton_subsistema,
)

# Color azul del logo
COLOR_AZUL_LOGO = "#125ca6"


def crear_bloque_acciones(frame_funcionalidades, traducciones, frame_visual):
    """
    Crea el bloque "Acciones" en la interfaz gráfica, que incluye botones para gestionar proyectos,
    subsistemas y asignaciones.

    Args:
        frame_funcionalidades (tk.Frame): Frame principal donde se colocan los bloques funcionales.
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        frame_visual (tk.Frame): Frame donde se visualizarán las opciones seleccionadas.

    Funcionalidad:
        - Crea un contenedor dentro del frame principal.
        - Agrega botones para proyectos, subsistemas y asignaciones con sus respectivas
          funcionalidades.
    """

    ### BLOQUE 3: ACCIONES
    # Crear el frame contenedor para el bloque de acciones.
    frame_acciones = tk.Frame(
        frame_funcionalidades,
        bg=COLOR_AZUL_LOGO,
        highlightbackground="#3790e9",
        highlightthickness=3,
        padx=5,
        pady=5,
    )  # Ajustamos padding
    frame_acciones.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    # Configurar la columna del frame_acciones para que se expanda
    frame_acciones.grid_columnconfigure(0, weight=1)

    # Botón Proyecto dentro del bloque 3
    boton_proyecto = tk.Button(
        frame_acciones,
        text=traducciones["P_PROYECTOS"],
        command=lambda: crear_boton_proyecto(
            traducciones, frame_acciones, frame_visual
        ),
    )
    boton_proyecto.grid(row=0, column=0, padx=10, pady=8, ipady=5, sticky="ew")

    # Botón Subsistema dentro del bloque 3
    boton_subsistema = tk.Button(
        frame_acciones,
        text=traducciones["P_SUBSISTEMA"],
        command=lambda: crear_boton_subsistema(
            traducciones, frame_acciones, frame_visual
        ),
    )
    boton_subsistema.grid(row=1, column=0, padx=10, pady=8, ipady=5, sticky="ew")

    # Botón Asignar dentro del bloque 3
    boton_asignar = tk.Button(
        frame_acciones,
        text=traducciones["P_ASIGNAR"],
        command=lambda: crear_boton_asignar(traducciones, frame_acciones, frame_visual),
    )
    boton_asignar.grid(row=2, column=0, padx=10, pady=8, ipady=5, sticky="ew")
