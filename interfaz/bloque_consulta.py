import tkinter as tk

# Función para limpiar el contenido del visualizador (por si es necesario en alguna funcionalidad)
def limpiar_visualizador(frame_visual):
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Función para crear el bloque de CONSULTA y los filtros adicionales
def crear_boton_consulta(frame_funcionalidades, frame_visual):
    # Botón de CONSULTA
    boton_consulta = tk.Button(frame_funcionalidades, text="CONSULTA")
    boton_consulta.grid(row=3, column=0, padx=10, pady=20, sticky="ew", ipady=10)

    # Crear el frame para los filtros de selección
    filtros_frame = tk.Frame(frame_funcionalidades, bg="lightgray")
    filtros_frame.grid(row=4, column=0, pady=10, sticky="ew")
    filtros_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    # Casillas de selección
    checkbox_requisitos = tk.Checkbutton(filtros_frame, text="Requisitos")
    checkbox_requisitos.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    checkbox_documentos = tk.Checkbutton(filtros_frame, text="Documentos")
    checkbox_documentos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    checkbox_proyectos = tk.Checkbutton(filtros_frame, text="Proyectos")
    checkbox_proyectos.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    checkbox_subsistemas = tk.Checkbutton(filtros_frame, text="Subsistemas")
    checkbox_subsistemas.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    # Filtros adicionales: Documentos, Subsistemas, Proyectos
    crear_bloque_filtros(frame_funcionalidades)

# Función para crear los tres cuadros de texto debajo de las casillas de selección
def crear_bloque_filtros(frame_funcionalidades):
    # Cuadro para Documentos
    label_documentos = tk.Label(frame_funcionalidades, text="Documentos", bg="lightgray")
    label_documentos.grid(row=5, column=0, padx=10, pady=5, sticky="w")

    entry_documentos = tk.Entry(frame_funcionalidades)
    entry_documentos.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

    # Cuadro para Subsistemas
    label_subsistemas = tk.Label(frame_funcionalidades, text="Subsistemas", bg="lightgray")
    label_subsistemas.grid(row=7, column=0, padx=10, pady=5, sticky="w")

    entry_subsistemas = tk.Entry(frame_funcionalidades)
    entry_subsistemas.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

    # Cuadro para Proyectos
    label_proyectos = tk.Label(frame_funcionalidades, text="Proyectos", bg="lightgray")
    label_proyectos.grid(row=9, column=0, padx=10, pady=5, sticky="w")

    entry_proyectos = tk.Entry(frame_funcionalidades)
    entry_proyectos.grid(row=10, column=0, padx=10, pady=5, sticky="ew")
