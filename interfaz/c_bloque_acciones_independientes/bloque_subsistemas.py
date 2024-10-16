import sys
import os
import tkinter as tk
from tkinter import messagebox
from almacenamiento.func_subsistemas import insertar_subsistema, obtener_subsistemas, borrar_subsistema

# Añade la carpeta raíz al sys.path para que Python pueda encontrar los módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    """Elimina todos los widgets dentro del frame_visual."""
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Función para agregar un subsistema
def agregar_subsistema(entry_subsistema, lista_subsistemas):
    """Inserta un nuevo subsistema en la base de datos y actualiza la lista."""
    subsistema = entry_subsistema.get()
    if subsistema:
        insertar_subsistema(subsistema)  # Llamada a la función para insertar en la BD
        entry_subsistema.delete(0, tk.END)  # Limpiar el campo de entrada
        mostrar_subsistemas(lista_subsistemas)  # Actualizar la lista de subsistemas
    else:
        messagebox.showerror("Error", "Por favor, ingrese un nombre de subsistema.")

# Función para mostrar todos los subsistemas
def mostrar_subsistemas(lista_subsistemas):
    """Muestra todos los subsistemas en la lista."""
    lista_subsistemas.delete(0, tk.END)
    subsistemas = obtener_subsistemas()  # Obtener subsistemas de la BD
    for subsistema in subsistemas:
        lista_subsistemas.insert(tk.END, f"ID: {subsistema[0]} - Nombre: {subsistema[1]}")
    return subsistemas

# Función para eliminar un subsistema
def eliminar_subsistema(entry_id_eliminar, lista_subsistemas):
    """Elimina un subsistema de la base de datos y actualiza la lista."""
    subsistema_id = entry_id_eliminar.get()
    if subsistema_id:
        borrar_subsistema(int(subsistema_id))  # Llamada para eliminar de la BD
        mostrar_subsistemas(lista_subsistemas)  # Actualizar la lista de subsistemas
    else:
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")

# Función para crear el bloque de Subsistema en el visualizador
def crear_boton_subsistema(frame_funcionalidades, frame_visual):
    """Crea el bloque de gestión de subsistemas (Agregar, Mostrar, Eliminar)."""
    # Limpiar visualizador antes de agregar nuevos widgets
    limpiar_visualizador(frame_visual)
    
    # Crear widgets en el visualizador
    label_subsistema = tk.Label(frame_visual, text="Nuevo Subsistema:", font=("Arial", 12))
    label_subsistema.pack(pady=5)
    
    entry_subsistema = tk.Entry(frame_visual)
    entry_subsistema.pack(pady=5)
    
    # Crear la lista de subsistemas
    lista_subsistemas = tk.Listbox(frame_visual, width=50)
    lista_subsistemas.pack(pady=10)
    
    # Botón para agregar subsistema
    boton_agregar = tk.Button(frame_visual, text="Agregar Subsistema", 
                              command=lambda: agregar_subsistema(entry_subsistema, lista_subsistemas))
    boton_agregar.pack(pady=10)

    # Mostrar subsistemas al inicio
    mostrar_subsistemas(lista_subsistemas)
    
    # Entrada y botón para eliminar subsistema
    label_id_eliminar = tk.Label(frame_visual, text="ID de Subsistema a Eliminar:", font=("Arial", 12))
    label_id_eliminar.pack(pady=5)
    
    entry_id_eliminar = tk.Entry(frame_visual)
    entry_id_eliminar.pack(pady=5)
    
    boton_eliminar = tk.Button(frame_visual, text="Eliminar Subsistema", 
                               command=lambda: eliminar_subsistema(entry_id_eliminar, lista_subsistemas))
    boton_eliminar.pack(pady=10)

def mostrar_subsistemas_combobox(combobox_subsistemas):
    """Muestra todos los subsistemas en el Combobox."""
    subsistemas = obtener_subsistemas()  # Obtener subsistemas de la BD
    # Extraer solo los nombres de los subsistemas (o el valor que quieras mostrar)
    lista_nombres_subsistemas = [subsistema[1] for subsistema in subsistemas]
    
    # Asignar los valores al combobox
    combobox_subsistemas['values'] = lista_nombres_subsistemas
    