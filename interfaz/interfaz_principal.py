import tkinter as tk
from PIL import Image, ImageTk
import os

# Importar funciones específicas de otros módulos
from .bloque_proyecto import crear_boton_proyecto
from .bloque_subsistema import crear_boton_subsistema
from .bloque_load import seleccionar_archivo, ventana_seleccionar_proyecto, aceptar_proyecto, cargar_documento
from .bloque_consulta import realizar_consulta, verificar_opcion_seleccionada

# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    """Elimina todos los widgets dentro del frame de visualización."""
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("RM Requirements Management")
ventana.state('zoomed')  # Maximizar la ventana

# Incluir el logo en la barra del software
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_icono = os.path.join(ruta_base, "logo_reducido.ico")  # Ruta del icono de la aplicación
ventana.iconbitmap(ruta_icono)  # Asignar icono a la ventana

# Crear el frame para las funcionalidades (parte izquierda)
frame_funcionalidades = tk.Frame(ventana, bg="lightgray", padx=20, pady=20)
frame_funcionalidades.grid(row=0, column=0, sticky="nsew")

# Crear el frame para la visualización (parte derecha)
frame_visual = tk.Frame(ventana, bg="white")
frame_visual.grid(row=0, column=1, sticky="nsew")

# Configurar la ventana para que el bloque gris esté dividido en dos partes (izquierda y derecha)
ventana.grid_columnconfigure(0, weight=1)#, uniform="group1")  # Parte izquierda para botones no respetaba la anchura neuva 1/4
ventana.grid_columnconfigure(1, weight=4)#, uniform="group1")  # Parte derecha para visualización
ventana.grid_rowconfigure(0, weight=1)

# Cargar imagen de fondo para la parte visual
ruta_fondo = os.path.join(ruta_base, "logofondo.png")  # Ruta de la imagen de fondo
imagen_fondo = Image.open(ruta_fondo)
imagen_fondo = imagen_fondo.resize((600, 400))  # Ajustar el tamaño de la imagen
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)  # Convertir la imagen a formato compatible con Tkinter
label_fondo = tk.Label(frame_visual, image=imagen_fondo_tk, bg="white")
label_fondo.pack(expand=True)

# Botón de LOAD
boton_load = tk.Button(
    frame_funcionalidades, text="LOAD", 
    command=lambda: ventana_seleccionar_proyecto(
        lambda proyecto_nombre, proyectos, ventana: aceptar_proyecto(
            proyecto_nombre, proyectos, ventana, entry_archivo, 
            lambda proyecto_id: cargar_documento(entry_archivo, proyecto_id, frame_visual))))
boton_load.grid(row=0, column=0, padx=10, pady=10, ipady=10, sticky="ew")

# Botón de Seleccionar archivo
boton_seleccionar = tk.Button(frame_funcionalidades, text="Seleccionar archivo", 
                              command=lambda: seleccionar_archivo(entry_archivo))
boton_seleccionar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Cuadro de texto para mostrar la ruta del archivo seleccionado
entry_archivo = tk.Entry(frame_funcionalidades)
entry_archivo.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Botón de CONSULTA
boton_consulta = tk.Button(
    frame_funcionalidades, text="CONSULTA", 
    command=lambda: realizar_consulta(
        verificar_opcion_seleccionada(var_requisitos, var_documentos, var_proyectos, var_subsistemas),
        entry_subsistemas, entry_proyectos, entry_documentos, frame_visual))
boton_consulta.grid(row=3, column=0, padx=10, pady=10, sticky="ew", ipady=10)

# Crear frame para filtros
filtros_frame = tk.Frame(frame_funcionalidades, bg="lightgray")
filtros_frame.grid(row=4, column=0, pady=10, sticky="ew")
filtros_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

# Variables para almacenar el estado de las opciones
var_requisitos = tk.BooleanVar()
var_documentos = tk.BooleanVar()
var_proyectos = tk.BooleanVar()
var_subsistemas = tk.BooleanVar()

# Casillas de selección para los filtros
checkbox_requisitos = tk.Checkbutton(filtros_frame, text="Requisitos", variable=var_requisitos)
checkbox_requisitos.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

checkbox_documentos = tk.Checkbutton(filtros_frame, text="Documentos", variable=var_documentos)
checkbox_documentos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

checkbox_proyectos = tk.Checkbutton(filtros_frame, text="Proyectos", variable=var_proyectos)
checkbox_proyectos.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

checkbox_subsistemas = tk.Checkbutton(filtros_frame, text="Subsistemas", variable=var_subsistemas)
checkbox_subsistemas.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

# Filtro de Subsistemas
label_subsistemas = tk.Label(frame_funcionalidades, text="Subsistemas", bg="lightgray")
label_subsistemas.grid(row=5, column=0, padx=10, pady=5, sticky="w")

entry_subsistemas = tk.Entry(frame_funcionalidades)
entry_subsistemas.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

# Filtro de Proyectos
label_proyectos = tk.Label(frame_funcionalidades, text="Proyectos", bg="lightgray")
label_proyectos.grid(row=7, column=0, padx=10, pady=5, sticky="w")

entry_proyectos = tk.Entry(frame_funcionalidades)
entry_proyectos.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

# Filtro de Documentos
label_documentos = tk.Label(frame_funcionalidades, text="Documentos", bg="lightgray")
label_documentos.grid(row=9, column=0, padx=10, pady=5, sticky="w")

entry_documentos = tk.Entry(frame_funcionalidades)
entry_documentos.grid(row=10, column=0, padx=10, pady=5, sticky="ew")

# Botón Proyecto / Ciudad
boton_proyecto = tk.Button(
    frame_funcionalidades, text="Proyecto / Ciudad", 
    command=lambda: crear_boton_proyecto(frame_funcionalidades, frame_visual))
boton_proyecto.grid(row=11, column=0, padx=10, pady=10, sticky="ew", ipady=10)

# Botón Subsistema
boton_subsistema = tk.Button(
    frame_funcionalidades, text="Subsistema", 
    command=lambda: crear_boton_subsistema(frame_funcionalidades, frame_visual))
boton_subsistema.grid(row=12, column=0, padx=10, pady=10, sticky="ew", ipady=10)

# Botón Asignar
boton_asignar = tk.Button(frame_funcionalidades, text="Asignar")
boton_asignar.grid(row=13, column=0, padx=10, pady=10, sticky="ew", ipady=10)

# Botón Eliminar
boton_eliminar = tk.Button(frame_funcionalidades, text="Eliminar")
boton_eliminar.grid(row=14, column=0, padx=10, pady=10, sticky="ew", ipady=10)

# Ejecutar el mainloop de la ventana
ventana.mainloop()
