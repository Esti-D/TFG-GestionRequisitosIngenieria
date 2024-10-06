import sys
import os
import tkinter as tk
from almacenamiento.func_ciudades import insertar_ciudad, obtener_ciudades, borrar_ciudad
from tkinter import messagebox

# Añade la carpeta raíz al sys.path para que Python pueda encontrar los módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    """Elimina todos los widgets del frame de visualización."""
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Función para crear el bloque de Proyecto / Ciudad en el visualizador
def crear_boton_proyecto(frame_funcionalidades, frame_visual):
    """Crea el interfaz para gestionar proyectos/ciudades en el frame de visualización."""
    
    # Función interna para agregar un nuevo proyecto/ciudad
    def agregar_ciudad():
        """Agrega una nueva ciudad/proyecto a la base de datos y actualiza la lista."""
        ciudad = entry_ciudad.get()  # Obtener el nombre del proyecto/ciudad
        if ciudad:
            insertar_ciudad(ciudad)  # Insertar ciudad en la base de datos
            entry_ciudad.delete(0, tk.END)  # Limpiar el campo de entrada
            mostrar_ciudades()  # Actualizar la lista con las nuevas ciudades
        else:
            tk.messagebox.showerror("Error", "Por favor, ingrese un nombre de proyecto/ciudad.")
    
    # Función interna para mostrar todos los proyectos/ciudades
    def mostrar_ciudades():
        """Muestra todos los proyectos/ciudades almacenados en la base de datos."""
        lista_ciudades.delete(0, tk.END)  # Limpiar la lista actual
        ciudades = obtener_ciudades()  # Obtener ciudades de la base de datos
        for ciudad in ciudades:
            lista_ciudades.insert(tk.END, f"ID: {ciudad[0]} - Nombre: {ciudad[1]}")  # Mostrar ciudades

    # Función interna para eliminar un proyecto/ciudad
    def eliminar_ciudad():
        """Elimina un proyecto/ciudad usando el ID proporcionado."""
        ciudad_id = entry_id_eliminar.get()  # Obtener el ID del proyecto a eliminar
        if ciudad_id:
            borrar_ciudad(int(ciudad_id))  # Eliminar la ciudad de la base de datos
            mostrar_ciudades()  # Actualizar la lista de ciudades
        else:
            tk.messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
    
    # Limpiar el contenido actual del visualizador antes de agregar los nuevos elementos
    limpiar_visualizador(frame_visual)
    
    # Crear widgets para agregar un nuevo proyecto/ciudad
    label_ciudad = tk.Label(frame_visual, text="Nuevo Proyecto / Ciudad:", font=("Arial", 12))
    label_ciudad.pack(pady=5)
    
    entry_ciudad = tk.Entry(frame_visual)  # Campo de entrada para el nombre del proyecto/ciudad
    entry_ciudad.pack(pady=5)
    
    boton_agregar = tk.Button(frame_visual, text="Agregar Proyecto / Ciudad", command=agregar_ciudad)
    boton_agregar.pack(pady=10)

    # Lista de proyectos/ciudades
    lista_ciudades = tk.Listbox(frame_visual, width=50)  # Listbox para mostrar proyectos/ciudades
    lista_ciudades.pack(pady=10)
    mostrar_ciudades()  # Llamar a la función para mostrar proyectos al inicio

    # Widgets para eliminar un proyecto/ciudad por ID
    label_id_eliminar = tk.Label(frame_visual, text="ID de Proyecto / Ciudad a Eliminar:", font=("Arial", 12))
    label_id_eliminar.pack(pady=5)
    
    entry_id_eliminar = tk.Entry(frame_visual)  # Campo de entrada para el ID del proyecto/ciudad a eliminar
    entry_id_eliminar.pack(pady=5)
    
    boton_eliminar = tk.Button(frame_visual, text="Eliminar Proyecto / Ciudad", command=eliminar_ciudad)
    boton_eliminar.pack(pady=10)
