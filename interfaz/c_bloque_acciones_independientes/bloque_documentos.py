import sys
import os

from interfaz.b_bloque_consulta.filtros import actualizar_combobox_documentos


# Añadir la ruta del directorio principal del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from almacenamiento.func_documentos import (
    insertar_documento,
    obtener_documentos,
    borrar_documento,
)


# interfaz de consulta
def crear_interfaz_documentos(frame_funcionalidades, frame_visual):

    # Función para agregar un nuevo documento
    def agregar_documento():
        titulo = entry_titulo.get()
        version = entry_version.get()
        ciudad_id = entry_ciudad_id.get()

        if titulo and version and ciudad_id:
            insertar_documento(titulo, version, int(ciudad_id))
            entry_titulo.delete(0, tk.END)
            entry_version.delete(0, tk.END)
            entry_ciudad_id.delete(0, tk.END)
            mostrar_documentos()
        else:
            tk.messagebox.showerror("Error", "Por favor, complete todos los campos.")

    # Función para mostrar todos los documentos
    def mostrar_documentos():
        lista_documentos.delete(0, tk.END)
        documentos = obtener_documentos()
        for documento in documentos:
            lista_documentos.insert(
                tk.END,
                f"ID: {documento[0]} - Título: {documento[1]} - Ciudad ID: {documento[3]}",
            )

    # Función para eliminar un documento por ID
    def eliminar_documento():
        documento_id = entry_id_eliminar.get()
        if documento_id:
            borrar_documento(int(documento_id))
            mostrar_documentos()
        else:
            tk.messagebox.showerror("Error", "Por favor, ingrese un ID válido.")

    # Crear widgets para documentos
    label_titulo = tk.Label(
        frame_funcionalidades, text="Título del Documento:", bg="lightgray"
    )
    label_titulo.pack(pady=5)
    entry_titulo = tk.Entry(frame_funcionalidades)
    entry_titulo.pack(pady=5)

    label_version = tk.Label(frame_funcionalidades, text="Versión:", bg="lightgray")
    label_version.pack(pady=5)
    entry_version = tk.Entry(frame_funcionalidades)
    entry_version.pack(pady=5)

    label_ciudad_id = tk.Label(frame_funcionalidades, text="Proyecto:", bg="lightgray")
    label_ciudad_id.pack(pady=5)
    entry_ciudad_id = tk.Entry(frame_funcionalidades)
    entry_ciudad_id.pack(pady=5)

    boton_agregar = tk.Button(
        frame_funcionalidades, text="Agregar Documento", command=agregar_documento
    )
    boton_agregar.pack(pady=10)

    # Lista de documentos
    lista_documentos = tk.Listbox(frame_visual, width=50)
    lista_documentos.pack(pady=10)
    mostrar_documentos()

    # Eliminar documento por ID
    label_id_eliminar = tk.Label(
        frame_funcionalidades, text="ID de Documento a Eliminar:", bg="lightgray"
    )
    label_id_eliminar.pack(pady=5)
    entry_id_eliminar = tk.Entry(frame_funcionalidades)
    entry_id_eliminar.pack(pady=5)
    boton_eliminar = tk.Button(
        frame_funcionalidades, text="Eliminar Documento", command=eliminar_documento
    )
    boton_eliminar.pack(pady=10)


def mostrar_documentos_combobox(traducciones, combobox_documentos):

    actualizar_combobox_documentos(traducciones, combobox_documentos)

    """Muestra todos los subsistemas en el Combobox."""
    documentos = obtener_documentos()  # Obtener subsistemas de la BD
    # Extraer solo los nombres de los subsistemas (o el valor que quieras mostrar)
    lista_nombres_documentos = [documento[1] for documento in documentos]

    # Asignar los valores al combobox
    combobox_documentos["values"] = lista_nombres_documentos


# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    """Elimina todos los widgets dentro del frame_visual."""
    for widget in frame_visual.winfo_children():
        widget.destroy()
