import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Importar funciones específicas de otros módulos
from .bloque_proyecto import crear_boton_proyecto
from .bloque_subsistema import crear_boton_subsistema, mostrar_subsistemas
from .bloque_load import seleccionar_archivo, ventana_seleccionar_proyecto, aceptar_proyecto, cargar_documento
from .bloque_consulta import realizar_consulta, verificar_opcion_seleccionada
from .bloque_ajustes import abrir_ajustes
from almacenamiento.func_subsistemas import obtener_subsistemas 

# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    """Elimina todos los widgets dentro del frame de visualización."""
    for widget in frame_visual.winfo_children():
        widget.destroy()


# Función principal que encapsula toda la lógica de la interfaz
def interfaz_principal(db_path):
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("RM Requirements Management")
    ventana.state('zoomed')  # Maximizar la ventana

    # Incluir el logo en la barra del software
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_icono = os.path.join(ruta_base, "logo_reducido.ico")  # Ruta del icono de la aplicación
    ventana.iconbitmap(ruta_icono)  # Asignar icono a la ventana

    # Configurar la ventana para que el bloque gris esté dividido en dos partes (izquierda y derecha)
    ventana.grid_columnconfigure(0, weight=1)  # Parte izquierda para botones
    ventana.grid_columnconfigure(1, weight=4)  # Parte derecha para visualización
    ventana.grid_rowconfigure(0, weight=1)

    # Crear el frame para la visualización (parte derecha)
    frame_visual = tk.Frame(ventana, bg="white")
    frame_visual.grid(row=0, column=1, sticky="nsew")

    # Cargar imagen de fondo para la parte visual
    ruta_fondo = os.path.join(ruta_base, "logofondo4.png")  # Ruta de la imagen de fondo
    imagen_fondo = Image.open(ruta_fondo)
    imagen_fondo = imagen_fondo.resize((800, 600))  # Ajustar el tamaño de la imagen
    imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)  # Convertir la imagen a formato compatible con Tkinter
    label_fondo = tk.Label(frame_visual, image=imagen_fondo_tk, bg="white")
    label_fondo.pack(expand=True)

    # Crear el frame para las funcionalidades (parte izquierda)
    frame_funcionalidades = tk.Frame(ventana, bg="#125ca6", padx=30, pady=20)  # #"lightgray" Ajustamos el padding para mayor expansión
    frame_funcionalidades.grid(row=0, column=0, sticky="nsew")

    # Configurar la expansión dentro del frame de funcionalidades
    frame_funcionalidades.grid_columnconfigure(0, weight=1)  # Aseguramos que la única columna ocupe todo el espacio

    # Color azul del logo 
    color_azul_logo = "#125ca6"

    ### BLOQUE 1: LOAD
    frame_load = tk.Frame(frame_funcionalidades, bg=color_azul_logo, highlightbackground="#3790e9", highlightthickness=3, padx=5, pady=3)  # Reducimos el padding en el frame
    frame_load.grid(row=0, column=0, padx=10, pady=8, sticky="ew")

    # Configurar la columna del frame_load para que se expanda
    frame_load.grid_columnconfigure(0, weight=1)

    # Botón de LOAD dentro del bloque 1
    boton_load = tk.Button(frame_load, text="LOAD", command=lambda: ventana_seleccionar_proyecto(
        lambda proyecto_nombre, proyectos, ventana: aceptar_proyecto(
            proyecto_nombre, proyectos, ventana, entry_archivo, 
            lambda proyecto_id: cargar_documento(entry_archivo, proyecto_id, frame_visual))))
    boton_load.grid(row=0, column=0, padx=10, pady=8, sticky="ew", ipady=8)

    # Botón de Seleccionar archivo dentro del bloque 1
    boton_seleccionar = tk.Button(frame_load, text="Seleccionar archivo", command=lambda: seleccionar_archivo(entry_archivo))
    boton_seleccionar.grid(row=1, column=0, padx=10, pady=8, sticky="ew")

    # Cuadro de texto para mostrar la ruta del archivo seleccionado dentro del bloque 1
    entry_archivo = tk.Entry(frame_load)
    entry_archivo.grid(row=2, column=0, padx=10, pady=5, sticky="ew")


    ### BLOQUE 2: CONSULTA
    frame_consulta = tk.Frame(frame_funcionalidades, bg=color_azul_logo, highlightbackground="#3790e9", highlightthickness=3,padx=5, pady=5)  # Ajustamos padding
    frame_consulta.grid(row=1, column=0, padx=10, pady=8, sticky="ew")

    # Configurar la columna del frame_consulta para que se expanda
    frame_consulta.grid_columnconfigure(0, weight=1)

    # Botón de CONSULTA dentro del bloque 2
    boton_consulta = tk.Button(frame_consulta, text="CONSULTA", command=lambda: realizar_consulta(
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
    checkbox_requisitos = tk.Checkbutton(filtros_frame, text="Requisitos", variable=var_requisitos, command=lambda: seleccionar_unico(var_requisitos))
    checkbox_requisitos.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    checkbox_documentos = tk.Checkbutton(filtros_frame, text="Documentos", variable=var_documentos, command=lambda: seleccionar_unico(var_documentos))
    checkbox_documentos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    checkbox_proyectos = tk.Checkbutton(filtros_frame, text="Proyectos", variable=var_proyectos, command=lambda: seleccionar_unico(var_proyectos))
    checkbox_proyectos.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    checkbox_subsistemas = tk.Checkbutton(filtros_frame, text="Subsistemas", variable=var_subsistemas, command=lambda: seleccionar_unico(var_subsistemas))
    checkbox_subsistemas.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    # Filtro de Subsistemas dentro del bloque 2
    label_subsistemas = tk.Label(frame_consulta, text="Subsistemas", bg="white")
    label_subsistemas.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    combobox_subsistemas = ttk.Combobox(frame_consulta, state="readonly", postcommand=lambda: mostrar_subsistemas(combobox_subsistemas))
    combobox_subsistemas.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    # Filtro de Proyectos dentro del bloque 2
    label_proyectos = tk.Label(frame_consulta, text="Proyectos", bg="white")
    label_proyectos.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    combobox_proyectos = ttk.Combobox(frame_consulta, state="readonly")
    combobox_proyectos.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

    # Filtro de Documentos dentro del bloque 2
    label_documentos = tk.Label(frame_consulta, text="Documentos", bg="white")
    label_documentos.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    combobox_documentos = ttk.Combobox(frame_consulta, state="readonly")
    combobox_documentos.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

    ### BLOQUE 3: ACCIONES
    frame_acciones = tk.Frame(frame_funcionalidades, bg=color_azul_logo, highlightbackground="#3790e9", highlightthickness=3,padx=5, pady=5)  # Ajustamos padding
    frame_acciones.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    # Configurar la columna del frame_acciones para que se expanda
    frame_acciones.grid_columnconfigure(0, weight=1)

    # Botón Proyecto / Ciudad dentro del bloque 3
    boton_proyecto = tk.Button(frame_acciones, text="Proyecto / Ciudad", command=lambda: crear_boton_proyecto(frame_acciones, frame_visual))
    boton_proyecto.grid(row=0, column=0, padx=10, pady=8, ipady=5, sticky="ew")

    # Botón Subsistema dentro del bloque 3
    boton_subsistema = tk.Button(frame_acciones, text="Subsistema", command=lambda: crear_boton_subsistema(frame_acciones, frame_visual))
    boton_subsistema.grid(row=1, column=0, padx=10, pady=8, ipady=5,sticky="ew")

    # Botón Asignar dentro del bloque 3
    boton_asignar = tk.Button(frame_acciones, text="Asignar")
    boton_asignar.grid(row=2, column=0, padx=10, pady=8, ipady=5, sticky="ew")

    # Botón Eliminar dentro del bloque 3
    boton_eliminar = tk.Button(frame_acciones, text="Eliminar")
    boton_eliminar.grid(row=3, column=0, padx=10, pady=8, ipady=5, sticky="ew")

    # Botón Ajustes (lo colocamos debajo de Eliminar)
    boton_ajustes = tk.Button(frame_funcionalidades, text="Ajustes", command=lambda: abrir_ajustes(frame_visual))
    boton_ajustes.grid(row=3, column=0, padx=10, pady=8, sticky="ew", ipady=8)

    # Ejecutar el mainloop de la ventana
    ventana.mainloop()

