import sys
import os
import tkinter as tk
from tkinter import messagebox


# Función para limpiar el contenido del visualizador
def limpiar_visualizador(frame_visual):
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Función para crear el bloque de Proyecto / Ciudad en el visualizador
def crear_boton_eliminar(traducciones, frame_funcionalidades, frame_visual):
    """Crea el interfaz eliminaciones en el frame de visualización."""

    # Limpiar el contenido actual del visualizador antes de agregar los nuevos elementos
    limpiar_visualizador(frame_visual)
        
    # Crear widgets para agregar un nuevo proyecto/ciudad
    label_eliminacion = tk.Label(frame_visual, text="Eliminar -Nuevo Proyecto / Ciudad:", font=("Arial", 12))
    label_eliminacion.pack(pady=5)
        
    entry_eliminacion = tk.Entry(frame_visual)  # Campo de entrada para el nombre del proyecto/ciudad
    entry_eliminacion.pack(pady=5)
        
    boton_eliminar = tk.Button(frame_visual, text="Eliminar - Agregar Proyecto / Ciudad", )
    boton_eliminar.pack(pady=10)

#Función para crear el bloque de Proyecto / Ciudad en el visualizador
def crear_boton_documento( frame_funcionalidades, frame_visual):
    """Crea el interfaz eliminaciones en el frame de visualización."""

    # Limpiar el contenido actual del visualizador antes de agregar los nuevos elementos
    limpiar_visualizador(frame_visual)
        
    # Crear widgets para agregar un nuevo proyecto/ciudad
    label_eliminacion = tk.Label(frame_visual, text="Eliminar -Nuevo Proyecto / Ciudad:", font=("Arial", 12))
    label_eliminacion.pack(pady=5)
        
    entry_eliminacion = tk.Entry(frame_visual)  # Campo de entrada para el nombre del proyecto/ciudad
    entry_eliminacion.pack(pady=5)
        
    boton_eliminar = tk.Button(frame_visual, text="Eliminar - Agregar Proyecto / Ciudad", )
    boton_eliminar.pack(pady=10)
        

