import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import sys

from .consulta_de import verificar_opcion_seleccionada, realizar_consulta, mostrar_resultados
from .filtros import actualizar_combobox
from interfaz.bloque_subsistema import mostrar_subsistemas_combobox 
from interfaz.bloque_proyecto import mostrar_proyectos_combobox 
#from interfaz.bloque_documento import mostrar_documentos_combobox 
#from interfaz.bloque_requisito import mostrar_requisitos_combobox 





# Color azul del logo 
color_azul_logo = "#125ca6"

def crear_bloque_consulta(frame_funcionalidades, traducciones, frame_visual):
    frame_consulta = tk.Frame(frame_funcionalidades, bg=color_azul_logo, highlightbackground="#3790e9", highlightthickness=3,padx=5, pady=5)  # Ajustamos padding
    frame_consulta.grid(row=1, column=0, padx=10, pady=8, sticky="ew")

    # Configurar la columna del frame_consulta para que se expanda
    frame_consulta.grid_columnconfigure(0, weight=1)

    # Botón de CONSULTA dentro del bloque 2
    boton_consulta = tk.Button(frame_consulta, text=traducciones["P_CONSULTA"], command=lambda: realizar_consulta(
        verificar_opcion_seleccionada(var_requisitos, var_documentos, var_proyectos, var_subsistemas),
        combobox_subsistemas, combobox_proyectos, combobox_documentos, frame_visual))
    boton_consulta.grid(row=0, column=0, padx=10, pady=8, ipady=5, sticky="ew")

    # Frame para filtros dentro del bloque 2
    filtros_frame = tk.Frame(frame_consulta, bg=color_azul_logo)
    filtros_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    filtros_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    # Variables para almacenar el estado de las opciones
    var_requisitos = tk.BooleanVar()
    var_documentos = tk.BooleanVar()
    var_proyectos = tk.BooleanVar()
    var_subsistemas = tk.BooleanVar()
    
    # Función que controla que solo un Checkbutton pueda estar seleccionado a la vez
    def seleccionar_unico(selected_var):
        # Deseleccionar los demás Checkbuttons
        if selected_var == var_requisitos:
            var_documentos.set(0)
            var_proyectos.set(0)
            var_subsistemas.set(0)
        elif selected_var == var_documentos:
            var_requisitos.set(0)
            var_proyectos.set(0)
            var_subsistemas.set(0)
        elif selected_var == var_proyectos:
            var_requisitos.set(0)
            var_documentos.set(0)
            var_subsistemas.set(0)
        elif selected_var == var_subsistemas:
            var_requisitos.set(0)
            var_documentos.set(0)
            var_proyectos.set(0)


    # Casillas de selección para los filtros dentro del bloque 2
    checkbox_requisitos = tk.Checkbutton(filtros_frame, text=traducciones["P_TICK_REQUISITOS"], variable=var_requisitos, command=lambda: seleccionar_unico(var_requisitos))
    checkbox_requisitos.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    checkbox_documentos = tk.Checkbutton(filtros_frame, text=traducciones["P_TICK_DOCUMENTOS"], variable=var_documentos, command=lambda: seleccionar_unico(var_documentos))
    checkbox_documentos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    checkbox_proyectos = tk.Checkbutton(filtros_frame, text=traducciones["P_TICK_PROYECTOS"], variable=var_proyectos, command=lambda: seleccionar_unico(var_proyectos))
    checkbox_proyectos.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    checkbox_subsistemas = tk.Checkbutton(filtros_frame, text=traducciones["P_TICK_SUBSISTEMAS"], variable=var_subsistemas, command=lambda: seleccionar_unico(var_subsistemas))
    checkbox_subsistemas.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    # Filtro de Subsistemas dentro del bloque 2
    label_subsistemas = tk.Label(frame_consulta, text=traducciones["P_FILTRO_SUBSISTEMAS"], bg="white")
    label_subsistemas.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    combobox_subsistemas = ttk.Combobox(frame_consulta, state="readonly",postcommand=lambda:mostrar_subsistemas_combobox(combobox_subsistemas))
    combobox_subsistemas.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    # Filtro de Proyectos dentro del bloque 2
    label_proyectos = tk.Label(frame_consulta, text=traducciones["P_FILTRO_PROYECTOS"], bg="white")
    label_proyectos.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    combobox_proyectos = ttk.Combobox(frame_consulta, state="readonly",postcommand=lambda:mostrar_proyectos_combobox(combobox_proyectos))
    combobox_proyectos.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

    # Filtro de Documentos dentro del bloque 2
    label_documentos = tk.Label(frame_consulta, text=traducciones["P_FILTRO_DOCUMENTOS"], bg="white")
    label_documentos.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    combobox_documentos = ttk.Combobox(frame_consulta, state="readonly",postcommand=lambda:mostrar_documentos_combobox(combobox_documentos))
    combobox_documentos.grid(row=7, column=0, padx=10, pady=5, sticky="ew")