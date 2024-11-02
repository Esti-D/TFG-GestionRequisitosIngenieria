import tkinter as tk
from tkinter import messagebox
from almacenamiento.func_relaciones import obtener_relaciones, insertar_relacion_documento_subsistema, borrar_relacion_documento_subsistema  # Funciones necesarias

# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    """Elimina todos los widgets dentro del frame_visual."""
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Función para mostrar todas las asociaciones actuales entre documentos y subsistemas
def mostrar_asociaciones(traducciones,lista_asociaciones):
    """Muestra todas las asociaciones en la lista."""
    lista_asociaciones.delete(0, tk.END)
    asociaciones = obtener_relaciones()  # Obtener asociaciones de la BD
    for asociacion in asociaciones:
        documento_id, subsistema_id = asociacion
        lista_asociaciones.insert(tk.END, f"{traducciones["T_ID_DOCUMENTO"]} {documento_id} - {traducciones["T_ID_SUBSISTEMA"]} {subsistema_id}")
    return asociaciones

# Función para agregar una asociación entre un documento y un subsistema
def agregar_asociacion(traducciones, entry_documento_id, entry_subsistema_id, lista_asociaciones):
    """Inserta una nueva asociación en la base de datos y actualiza la lista."""
    documento_id = entry_documento_id.get()
    subsistema_id = entry_subsistema_id.get()
    if documento_id and subsistema_id:
        insertar_relacion_documento_subsistema(int(documento_id), int(subsistema_id))  # Llamada para insertar en la BD
        mostrar_asociaciones(traducciones,lista_asociaciones)  # Actualizar la lista de asociaciones
        entry_documento_id.delete(0, tk.END)  # Limpiar el campo de entrada
        entry_subsistema_id.delete(0, tk.END)  # Limpiar el campo de entrada
    else:
        messagebox.showerror(traducciones["M_Error"], traducciones["M_Ingrese_IDs_validos_documento_subsistema"])

# Función para eliminar una asociación
def eliminar_asociacion(traducciones, entry_documento_id, entry_subsistema_id, lista_asociaciones):
    """Elimina una asociación de la base de datos y actualiza la lista."""
    documento_id = entry_documento_id.get()
    subsistema_id = entry_subsistema_id.get()
    if documento_id and subsistema_id:
        borrar_relacion_documento_subsistema(int(documento_id), int(subsistema_id))  # Llamada para eliminar de la BD
        mostrar_asociaciones(traducciones,lista_asociaciones)  # Actualizar la lista de asociaciones
        entry_documento_id.delete(0, tk.END)  # Limpiar el campo de entrada
        entry_subsistema_id.delete(0, tk.END)  # Limpiar el campo de entrada
    else:
        messagebox.showerror("Error", "Por favor, ingrese IDs válidos para documento y subsistema.")

# Función para crear el bloque de "Asignar" en el visualizador
def crear_boton_asignar(traducciones,frame_funcionalidades, frame_visual):
    """Crea el bloque de gestión de asociaciones (Agregar, Mostrar, Eliminar)."""
    # Limpiar visualizador antes de agregar nuevos widgets
    limpiar_visualizador(frame_visual)
    
    # Crear widgets en el visualizador
    label_asociacion = tk.Label(frame_visual, text=traducciones["A_NUEVA_Asociocion"], font=("Arial", 12))
    label_asociacion.pack(pady=5)
    
    entry_documento_id = tk.Entry(frame_visual)
    entry_documento_id.pack(pady=5)
    entry_documento_id.insert(0, traducciones["T_ID_DOCUMENTO"])
    
    entry_subsistema_id = tk.Entry(frame_visual)
    entry_subsistema_id.pack(pady=5)
    entry_subsistema_id.insert(0, traducciones["T_ID_SUBSISTEMA"])
    
    # Crear la lista de asociaciones
    lista_asociaciones = tk.Listbox(frame_visual, width=50)
    lista_asociaciones.pack(pady=10)
    
    # Botón para agregar asociación
    boton_agregar = tk.Button(frame_visual, text=traducciones["A_Agregar_Asociacion"], 
                              command=lambda: agregar_asociacion(traducciones, entry_documento_id, entry_subsistema_id, lista_asociaciones))
    boton_agregar.pack(pady=10)

    # Mostrar asociaciones al inicio
    mostrar_asociaciones(traducciones, lista_asociaciones)
    
    # Entrada y botón para eliminar asociación
    label_id_eliminar = tk.Label(frame_visual, text=traducciones["A_Eliminar_Asociacion"], font=("Arial", 12))
    label_id_eliminar.pack(pady=5)
    
    entry_id_documento_eliminar = tk.Entry(frame_visual)
    entry_id_documento_eliminar.pack(pady=5)
    entry_id_documento_eliminar.insert(0, traducciones["T_ID_DOCUMENTO"])
    
    entry_id_subsistema_eliminar = tk.Entry(frame_visual)
    entry_id_subsistema_eliminar.pack(pady=5)
    entry_id_subsistema_eliminar.insert(0, traducciones["T_ID_SUBSISTEMA"])
    
    boton_eliminar = tk.Button(frame_visual, text=traducciones["A_Eliminar_Asociacion"], 
                               command=lambda: eliminar_asociacion(traducciones, entry_id_documento_eliminar, entry_id_subsistema_eliminar, lista_asociaciones))
    boton_eliminar.pack(pady=10)

