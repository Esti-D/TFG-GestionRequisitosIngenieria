import tkinter as tk

# Función para crear el botón LOAD y selección de archivos
def crear_boton_load(frame_funcionalidades):
    # Botón para cargar el archivo (LOAD)
    boton_load = tk.Button(frame_funcionalidades, text="LOAD")
    boton_load.grid(row=0, column=0, padx=10, pady=10, sticky="ew", ipady=10)

    # Botón para abrir explorador de archivos
    boton_seleccionar = tk.Button(frame_funcionalidades, text="Seleccionar archivo")
    boton_seleccionar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Cuadro de texto para mostrar la ruta seleccionada (debajo de seleccionar archivo)
    entry_archivo = tk.Entry(frame_funcionalidades)
    entry_archivo.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Función para crear los filtros de búsqueda y las casillas de selección
def crear_campos_filtros(frame_funcionalidades):
    # Botón de CONSULTA
    boton_consulta = tk.Button(frame_funcionalidades, text="CONSULTA")
    boton_consulta.grid(row=3, column=0, padx=10, pady=20, sticky="ew", ipady=10)

    # Crear el frame para los filtros (Requisitos, Documentos, Proyectos, Subsistemas)
    filtros_frame = tk.Frame(frame_funcionalidades, bg="lightgray")
    filtros_frame.grid(row=4, column=0, pady=10, sticky="ew")
    filtros_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Distribución horizontal

    # Filtros debajo del botón CONSULTA, distribuidos horizontalmente
    checkbox_requisitos = tk.Checkbutton(filtros_frame, text="Requisitos")
    checkbox_requisitos.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    checkbox_documentos = tk.Checkbutton(filtros_frame, text="Documentos")
    checkbox_documentos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    checkbox_proyectos = tk.Checkbutton(filtros_frame, text="Proyectos")
    checkbox_proyectos.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    checkbox_subsistemas = tk.Checkbutton(filtros_frame, text="Subsistemas")
    checkbox_subsistemas.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    # Crear el bloque de filtros (tres cuadros)
    crear_bloque_filtros(frame_funcionalidades)

# Función para crear los tres cuadros de filtros (Documentos, Subsistemas, Proyectos)
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

# Función para crear los botones adicionales (Proyecto/Ciudad, Subsistema, etc.)
def crear_botones_adicionales(frame_funcionalidades):
    # Botón Proyecto/Ciudad
    boton_proyecto = tk.Button(frame_funcionalidades, text="Proyecto / Ciudad")
    boton_proyecto.grid(row=11, column=0, padx=10, pady=10, sticky="ew", ipady=10)

    # Botón Subsistema
    boton_subsistema = tk.Button(frame_funcionalidades, text="Subsistema")
    boton_subsistema.grid(row=12, column=0, padx=10, pady=10, sticky="ew", ipady=10)

    # Botón Asignar
    boton_asignar = tk.Button(frame_funcionalidades, text="Asignar")
    boton_asignar.grid(row=13, column=0, padx=10, pady=10, sticky="ew", ipady=10)

    # Botón Eliminar
    boton_eliminar = tk.Button(frame_funcionalidades, text="Eliminar")
    boton_eliminar.grid(row=14, column=0, padx=10, pady=10, sticky="ew", ipady=10)
