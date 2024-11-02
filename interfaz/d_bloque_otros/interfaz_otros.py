import tkinter as tk
from tkinter import filedialog
import os
import sys

from interfaz.d_bloque_otros.ayuda.bloque_ayuda import abrir_ayuda
from interfaz.d_bloque_otros.opciones_ajustes import abrir_ajustes


def crear_bloque_otros(frame_funcionalidades, traducciones, frame_visual):

    
    # Frame contenedor para los botones Ajustes y Ayuda en la misma fila
    frame_ajustes_ayuda = tk.Frame(frame_funcionalidades, bg="#125ca6")
    frame_ajustes_ayuda.grid(row=3, column=0, padx=10, pady=8, sticky="ew")

    # Configurar columnas dentro del frame para que ambos botones ocupen la mitad del espacio
    frame_ajustes_ayuda.grid_columnconfigure(0, weight=1)
    frame_ajustes_ayuda.grid_columnconfigure(1, weight=1)

    # Botón Ajustes 
    boton_ajustes = tk.Button(frame_ajustes_ayuda, text=traducciones["P_AJUSTES"], command=lambda: abrir_ajustes(traducciones,frame_visual))
    boton_ajustes.grid(row=3, column=0, padx=5, pady=8, sticky="ew", ipady=8)
    
    # Botón Ayuda
    boton_ayuda = tk.Button(frame_ajustes_ayuda, text=traducciones["P_AYUDA"], command=lambda: abrir_ayuda(traducciones, frame_visual))
    boton_ayuda.grid(row=3, column=1, padx=5, pady=8, sticky="ew", ipady=8)