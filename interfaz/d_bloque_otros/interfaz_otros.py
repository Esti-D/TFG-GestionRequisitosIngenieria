"""
Archivo: interfaz_otros.py
Descripción: Este archivo contiene funciones para crear el bloque "Otros" en la interfaz de usuario,
que incluye los botones de "Ajustes" y "Ayuda".

Autor: Estíbalitz Díez
Fecha: 26/12/2024
Versión: 2
"""

import tkinter as tk
from interfaz.d_bloque_otros.ayuda.bloque_ayuda import abrir_ayuda
from interfaz.d_bloque_otros.opciones_ajustes import abrir_ajustes


def crear_bloque_otros(frame_funcionalidades, traducciones, frame_visual):
    """
    Crea el bloque "Otros" en la interfaz, que contiene los botones de "Ajustes" y "Ayuda".

    Args:
        frame_funcionalidades (tk.Frame): Frame principal donde se colocan los bloques funcionales.
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        frame_visual (tk.Frame): Frame donde se visualizan las opciones seleccionadas.

    Funcionalidad:
        - Crea un contenedor para los botones de Ajustes y Ayuda.
        - Coloca ambos botones en la misma fila y configura su distribución.
        - Los botones ejecutan las funciones correspondientes para abrir Ajustes o Ayuda.
    """

    # Frame contenedor para los botones Ajustes y Ayuda en la misma fila
    frame_ajustes_ayuda = tk.Frame(frame_funcionalidades, bg="#125ca6")
    frame_ajustes_ayuda.grid(row=3, column=0, padx=10, pady=8, sticky="ew")

    # Configurar columnas dentro del frame para que ambos botones ocupen la mitad del espacio
    frame_ajustes_ayuda.grid_columnconfigure(0, weight=1)
    frame_ajustes_ayuda.grid_columnconfigure(1, weight=1)

    # Botón Ajustes
    boton_ajustes = tk.Button(
        frame_ajustes_ayuda,
        text=traducciones["P_AJUSTES"],
        command=lambda: abrir_ajustes(traducciones, frame_visual),
    )
    boton_ajustes.grid(row=3, column=0, padx=5, pady=8, sticky="ew", ipady=8)

    # Botón Ayuda
    boton_ayuda = tk.Button(
        frame_ajustes_ayuda,
        text=traducciones["P_AYUDA"],
        command=lambda: abrir_ayuda(traducciones, frame_visual),
    )
    boton_ayuda.grid(row=3, column=1, padx=5, pady=8, sticky="ew", ipady=8)
