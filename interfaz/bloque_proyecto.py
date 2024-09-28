import sys
import os

# Añade la carpeta raíz al sys.path para que Python pueda encontrar los módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from almacenamiento.func_ciudades import insertar_ciudad, obtener_ciudades, borrar_ciudad
from tkinter import messagebox

# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Función para crear el bloque de Proyecto / Ciudad en el visualizador
def crear_boton_proyecto(frame_funcionalidades, frame_visual):
    # Función para agregar un nuevo proyecto/ciudad
    def agregar_ciudad():
        ciudad = entry_ciudad.get()
        if ciudad:
            insertar_ciudad(ciudad)
            entry_ciudad.delete(0, tk.END)  # Limpiar el campo de entrada
            mostrar_ciudades()  # Actualizar la lista
        else:
            tk.messagebox.showerror("Error", "Por favor, ingrese un nombre de proyecto/ciudad.")
    
    # Función para mostrar todos los proyectos/ciudades
    def mostrar_ciudades():
        lista_ciudades.delete(0, tk.END)  # Limpiar la lista
        ciudades = obtener_ciudades()
        for ciudad in ciudades:
            lista_ciudades.insert(tk.END, f"ID: {ciudad[0]} - Nombre: {ciudad[1]}")
    
    # Función para eliminar un proyecto/ciudad
    def eliminar_ciudad():
        ciudad_id = entry_id_eliminar.get()
        if ciudad_id:
            borrar_ciudad(int(ciudad_id))
            mostrar_ciudades()  # Actualizar la lista
        else:
            tk.messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
    
    # Limpiar el contenido actual del visualizador antes de agregar los nuevos elementos
    limpiar_visualizador(frame_visual)
    
    # Crear widgets para agregar un proyecto/ciudad
    label_ciudad = tk.Label(frame_visual, text="Nuevo Proyecto / Ciudad:", font=("Arial", 12))
    label_ciudad.pack(pady=5)
    entry_ciudad = tk.Entry(frame_visual)
    entry_ciudad.pack(pady=5)
    boton_agregar = tk.Button(frame_visual, text="Agregar Proyecto / Ciudad", command=agregar_ciudad)
    boton_agregar.pack(pady=10)

    # Lista de proyectos/ciudades
    lista_ciudades = tk.Listbox(frame_visual, width=50)
    lista_ciudades.pack(pady=10)
    mostrar_ciudades()  # Llamar al inicio para mostrar los proyectos/ciudades

    # Eliminar proyecto/ciudad por ID
    label_id_eliminar = tk.Label(frame_visual, text="ID de Proyecto / Ciudad a Eliminar:", font=("Arial", 12))
    label_id_eliminar.pack(pady=5)
    entry_id_eliminar = tk.Entry(frame_visual)
    entry_id_eliminar.pack(pady=5)
    boton_eliminar = tk.Button(frame_visual, text="Eliminar Proyecto / Ciudad", command=eliminar_ciudad)
    boton_eliminar.pack(pady=10)
