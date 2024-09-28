import sys
import os

# Añadir la ruta del directorio principal del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
#from tkinter import messagebox

from almacenamiento.func_ciudades import insertar_ciudad, obtener_ciudades, borrar_ciudad

def crear_interfaz_ciudades(frame_funcionalidades, frame_visual):
    # Función para agregar una nueva ciudad
    def agregar_ciudad():
        ciudad = entry_ciudad.get()
        if ciudad:
            insertar_ciudad(ciudad)
            entry_ciudad.delete(0, tk.END)  # Limpiar campo de entrada
            mostrar_ciudades()  # Actualizar la lista
        else:
            tk.messagebox.showerror("Error", "Por favor, ingrese un nombre de ciudad.")
    
    # Función para mostrar todas las ciudades
    def mostrar_ciudades():
        lista_ciudades.delete(0, tk.END)  # Limpiar la lista
        ciudades = obtener_ciudades()
        for ciudad in ciudades:
            lista_ciudades.insert(tk.END, f"ID: {ciudad[0]} - Nombre: {ciudad[1]}")

    # Función para eliminar una ciudad
    def eliminar_ciudad():
        ciudad_id = entry_id_eliminar.get()
        if ciudad_id:
            borrar_ciudad(int(ciudad_id))
            mostrar_ciudades()  # Actualizar la lista
        else:
            tk.messagebox.showerror("Error", "Por favor, ingrese un ID válido.")

    # Crear widgets para ciudades
    label_ciudad = tk.Label(frame_funcionalidades, text="Nueva Ciudad:", bg="lightgray")
    label_ciudad.pack(pady=5)
    entry_ciudad = tk.Entry(frame_funcionalidades)
    entry_ciudad.pack(pady=5)
    boton_agregar = tk.Button(frame_funcionalidades, text="Agregar Ciudad", command=agregar_ciudad)
    boton_agregar.pack(pady=10)

    # Lista de ciudades
    lista_ciudades = tk.Listbox(frame_visual, width=50)
    lista_ciudades.pack(pady=10)
    mostrar_ciudades()  # Llamar al inicio para mostrar las ciudades

    # Eliminar ciudad por ID
    label_id_eliminar = tk.Label(frame_funcionalidades, text="ID de Ciudad a Eliminar:", bg="lightgray")
    label_id_eliminar.pack(pady=5)
    entry_id_eliminar = tk.Entry(frame_funcionalidades)
    entry_id_eliminar.pack(pady=5)
    boton_eliminar = tk.Button(frame_funcionalidades, text="Eliminar Ciudad", command=eliminar_ciudad)
    boton_eliminar.pack(pady=10)

