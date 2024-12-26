"""
Archivo: bloque_proyectos.py
Descripción: Este archivo contiene funciones para gestionar proyectos o ciudades en la aplicación.
Permite crear, mostrar y eliminar proyectos mediante interacción con la interfaz gráfica.

Autor: Estíbalitz Díez
Fecha: 26/12/2024
Versión: 2
"""

import sys
import os
import tkinter as tk
from almacenamiento.func_proyectos import (
    insertar_proyecto,
    obtener_proyectos,
    borrar_proyecto,
)
from interfaz.b_bloque_consulta.filtros import actualizar_combobox_proyectos

# Añade la carpeta raíz al sys.path para que Python pueda encontrar los módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    """
    Elimina todos los widgets del frame de visualización.

    Args:
        frame_visual (tk.Frame): Frame que será limpiado.
    """
    for widget in frame_visual.winfo_children():
        widget.destroy()


# Función para crear el bloque de Proyecto / Ciudad en el visualizador
def crear_boton_proyecto(traducciones, frame_funcionalidades, frame_visual):
    """
    Crea el interfaz para gestionar proyectos o ciudades en el frame de visualización.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        frame_funcionalidades (tk.Frame): Frame principal de la interfaz.
        frame_visual (tk.Frame): Frame donde se mostrarán los widgets relacionados con proyectos.
    """

    # Función interna para agregar un nuevo proyecto/ciudad
    def agregar_proyecto():
        """Agrega una nueva ciudad/proyecto a la base de datos y actualiza la lista."""
        proyecto = entry_proyecto.get()  # Obtener el nombre del proyecto/ciudad
        if proyecto:
            insertar_proyecto(proyecto)  # Insertar ciudad en la base de datos
            entry_proyecto.delete(0, tk.END)  # Limpiar el campo de entrada
            mostrar_proyectos()  # Actualizar la lista con las nuevas ciudades
        else:
            tk.messagebox.showerror(
                traducciones["M_Error"], traducciones["M_Ingrese_un_nombre_de_proyecto"]
            )

    # Función interna para mostrar todos los proyectos/ciudades
    def mostrar_proyectos():
        """Muestra todos los proyectos/ciudades almacenados en la base de datos."""
        lista_proyectos.delete(0, tk.END)  # Limpiar la lista actual
        proyectos = obtener_proyectos()  # Obtener ciudades de la base de datos
        for proyecto in proyectos:
            lista_proyectos.insert(
                tk.END,
                f"ID: {proyecto[0]} - {traducciones["T_Nombre_proyecto"]}: {proyecto[1]}",
            )  # Mostrar ciudades

    # Función interna para eliminar un proyecto/ciudad
    def eliminar_proyecto():
        """Elimina un proyecto/ciudad usando el ID proporcionado."""
        proyecto_id = entry_id_eliminar.get()  # Obtener el ID del proyecto a eliminar
        if proyecto_id:
            borrar_proyecto(int(proyecto_id))  # Eliminar la ciudad de la base de datos
            mostrar_proyectos()  # Actualizar la lista de ciudades
        else:
            tk.messagebox.showerror(
                traducciones["M_Error"], traducciones["M_Ingrese_un_ID_valido"]
            )

    # Limpiar el contenido actual del visualizador antes de agregar los nuevos elementos
    limpiar_visualizador(frame_visual)

    # Crear widgets para agregar un nuevo proyecto/ciudad
    label_proyecto = tk.Label(
        frame_visual, text=traducciones["A_NUEVO_Proyecto"], font=("Arial", 12)
    )
    label_proyecto.pack(pady=5)

    entry_proyecto = tk.Entry(
        frame_visual
    )  # Campo de entrada para el nombre del proyecto/ciudad
    entry_proyecto.pack(pady=5)

    boton_agregar = tk.Button(
        frame_visual, text=traducciones["A_Agregar_Proyecto"], command=agregar_proyecto
    )
    boton_agregar.pack(pady=10)

    # Lista de proyectos/ciudades
    lista_proyectos = tk.Listbox(
        frame_visual, width=50
    )  # Listbox para mostrar proyectos/ciudades
    lista_proyectos.pack(pady=10)
    mostrar_proyectos()  # Llamar a la función para mostrar proyectos al inicio

    # Widgets para eliminar un proyecto/ciudad por ID
    label_id_eliminar = tk.Label(
        frame_visual,
        text=traducciones["A_ID_de_Proyecto_a_Eliminar"],
        font=("Arial", 12),
    )
    label_id_eliminar.pack(pady=5)

    entry_id_eliminar = tk.Entry(
        frame_visual
    )  # Campo de entrada para el ID del proyecto/ciudad a eliminar
    entry_id_eliminar.pack(pady=5)

    boton_eliminar = tk.Button(
        frame_visual,
        text=traducciones["A_Eliminar_Proyecto"],
        command=eliminar_proyecto,
    )
    boton_eliminar.pack(pady=10)


def mostrar_proyectos_combobox(traducciones, combobox_proyectos):
    """
    Muestra todos los proyectos en el Combobox.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        combobox_proyectos (ttk.Combobox): Combobox donde se mostrarán los proyectos.
    """
    actualizar_combobox_proyectos(traducciones, combobox_proyectos)

    proyectos = obtener_proyectos()  # Obtener subsistemas de la BD
    # Extraer solo los nombres de los subsistemas (o el valor que quieras mostrar)
    lista_nombres_proyectos = [proyecto[1] for proyecto in proyectos]

    # Asignar los valores al combobox
    combobox_proyectos["values"] = lista_nombres_proyectos
