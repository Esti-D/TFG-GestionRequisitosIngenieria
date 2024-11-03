import tkinter as tk
from tkinter import messagebox
from almacenamiento.func_documentos import (
    obtener_documentos,
)  # función de consulta de documentos
from almacenamiento.func_subsistemas import (
    obtener_subsistemas,
)  # funcion de consulta de subssistemas
from almacenamiento.func_proyectos import (
    obtener_proyectos,
)  # funcion de consulta de proyectos


def actualizar_combobox_subsistemas(traducciones, combobox_subsistemas):

    default_opcion = traducciones["O_TODOS"]

    # Obtener todos los subsistemas
    subsistemas = (
        obtener_subsistemas()
    )  # Debería devolver una lista de tuplas [(id_subsistema, nombre_subsistema), ...]
    combobox_subsistemas["values"] = [default_opcion] + [
        s[1] for s in subsistemas
    ]  # Solo muestra los nombres
    if subsistemas:
        combobox_subsistemas.current(0)  # Selecciona el primer subsistema por defecto


def actualizar_combobox_proyectos(traducciones, combobox_proyectos):

    default_opcion = traducciones["O_TODOS"]
    # Obtener todos los proyectos
    proyectos = (
        obtener_proyectos()
    )  # Debería devolver una lista de tuplas [(id_proyecto, nombre_proyecto), ...]
    combobox_proyectos["values"] = [default_opcion] + [
        p[1] for p in proyectos
    ]  # Solo muestra los nombres en el Combobox
    if proyectos:
        combobox_proyectos.current(0)  # Selecciona el primer proyecto por defecto


def actualizar_combobox_documentos(traducciones, combobox_documentos):

    default_opcion = traducciones["O_TODOS"]

    # Obtener todos los documentos
    documentos = (
        obtener_documentos()
    )  # Debería devolver una lista de tuplas [(id_documento, titulo_documento), ...]
    combobox_documentos["values"] = [default_opcion] + [
        d[1] for d in documentos
    ]  # Solo muestra los títulos
    if documentos:
        combobox_documentos.current(0)  # Selecciona el primer documento por defecto
