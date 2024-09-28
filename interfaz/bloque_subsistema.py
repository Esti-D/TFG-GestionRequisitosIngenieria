import sys
import os

# Añade la carpeta raíz al sys.path para que Python pueda encontrar los módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from almacenamiento.func_subsistemas import insertar_subsistema, obtener_subsistemas, borrar_subsistema

# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Función para crear el bloque de Subsistema en el visualizador
def crear_boton_subsistema(frame_funcionalidades, frame_visual):
    def agregar_subsistema():
        subsistema = entry_subsistema.get()
        if subsistema:
            insertar_subsistema(subsistema)
            entry_subsistema.delete(0, tk.END)  # Limpiar el campo de entrada
            mostrar_subsistemas()
        else:
            tk.messagebox.showerror("Error", "Por favor, ingrese un nombre de subsistema.")
    
    def mostrar_subsistemas():
        lista_subsistemas.delete(0, tk.END)
        subsistemas = obtener_subsistemas()
        for subsistema in subsistemas:
            lista_subsistemas.insert(tk.END, f"ID: {subsistema[0]} - Nombre: {subsistema[1]}")
    
    def eliminar_subsistema():
        subsistema_id = entry_id_eliminar.get()
        if subsistema_id:
            borrar_subsistema(int(subsistema_id))
            mostrar_subsistemas()
        else:
            tk.messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
    
    # Limpiar visualizador antes de agregar nuevos widgets
    limpiar_visualizador(frame_visual)
    
    # Crear widgets en el visualizador
    label_subsistema = tk.Label(frame_visual, text="Nuevo Subsistema:", font=("Arial", 12))
    label_subsistema.pack(pady=5)
    entry_subsistema = tk.Entry(frame_visual)
    entry_subsistema.pack(pady=5)
    boton_agregar = tk.Button(frame_visual, text="Agregar Subsistema", command=agregar_subsistema)
    boton_agregar.pack(pady=10)

    lista_subsistemas = tk.Listbox(frame_visual, width=50)
    lista_subsistemas.pack(pady=10)
    mostrar_subsistemas()

    label_id_eliminar = tk.Label(frame_visual, text="ID de Subsistema a Eliminar:", font=("Arial", 12))
    label_id_eliminar.pack(pady=5)
    entry_id_eliminar = tk.Entry(frame_visual)
    entry_id_eliminar.pack(pady=5)
    boton_eliminar = tk.Button(frame_visual, text="Eliminar Subsistema", command=eliminar_subsistema)
    boton_eliminar.pack(pady=10)
