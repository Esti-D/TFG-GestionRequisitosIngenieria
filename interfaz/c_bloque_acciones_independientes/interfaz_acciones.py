import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import sys

from interfaz.c_bloque_acciones_independientes.bloque_asignaciones import crear_boton_asignar
from interfaz.c_bloque_acciones_independientes.bloque_eliminaciones import crear_boton_eliminar
from interfaz.c_bloque_acciones_independientes.bloque_proyectos import crear_boton_proyecto
from interfaz.c_bloque_acciones_independientes.bloque_subsistemas import crear_boton_subsistema

# Color azul del logo 
color_azul_logo = "#125ca6"

def crear_bloque_acciones(frame_funcionalidades, traducciones, frame_visual):
    ### BLOQUE 3: ACCIONES
    frame_acciones = tk.Frame(frame_funcionalidades, bg=color_azul_logo, highlightbackground="#3790e9", highlightthickness=3,padx=5, pady=5)  # Ajustamos padding
    frame_acciones.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    # Configurar la columna del frame_acciones para que se expanda
    frame_acciones.grid_columnconfigure(0, weight=1)

    # Botón Proyecto dentro del bloque 3
    boton_proyecto = tk.Button(frame_acciones, text=traducciones["P_PROYECTOS"], command=lambda: crear_boton_proyecto(frame_acciones, frame_visual))
    boton_proyecto.grid(row=0, column=0, padx=10, pady=8, ipady=5, sticky="ew")

    # Botón Subsistema dentro del bloque 3
    boton_subsistema = tk.Button(frame_acciones, text=traducciones["P_SUBSISTEMA"], command=lambda: crear_boton_subsistema(frame_acciones, frame_visual))
    boton_subsistema.grid(row=1, column=0, padx=10, pady=8, ipady=5,sticky="ew")

    # Botón Asignar dentro del bloque 3
    boton_asignar = tk.Button(frame_acciones, text=traducciones["P_ASIGNAR"], command=lambda: crear_boton_asignar(frame_acciones, frame_visual))
    boton_asignar.grid(row=2, column=0, padx=10, pady=8, ipady=5, sticky="ew")

    # Botón Eliminar dentro del bloque 3
    boton_eliminar = tk.Button(frame_acciones, text=traducciones["P_ELIMINAR"], command=lambda: crear_boton_eliminar(frame_acciones, frame_visual))
    boton_eliminar.grid(row=3, column=0, padx=10, pady=8, ipady=5, sticky="ew")