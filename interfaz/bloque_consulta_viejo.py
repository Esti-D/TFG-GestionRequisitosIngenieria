import tkinter as tk
from tkinter import messagebox
from almacenamiento.func_documentos import obtener_documentos #función de consulta de documentos
from almacenamiento.func_subsistemas import obtener_subsistemas #funcion de consulta de subssistemas
from almacenamiento.func_requisitos import obtener_requisitos # funcion de consulta de requisitos
from almacenamiento.func_ciudades import obtener_ciudades # funcion de consulta de proyectos
from almacenamiento.func_documentos import obtener_documentos_filtrados #funcion de consulta de doc filtrados
from almacenamiento.func_subsistemas import obtener_subsistemas_filtrados #funcion de consulta de subsistemas filtrados

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
    #crear_bloque_filtros(frame_funcionalidades)

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

#funcion para verificar que opcion se ha escogido para realizar la consulta
def verificar_opcion_seleccionada(var_requisitos, var_documentos, var_proyectos, var_subsistemas):
    print(f"Requisitos:{var_requisitos.get()},Documentos: {var_documentos.get()},Proyectos: {var_proyectos.get()},Subsistemas:{var_subsistemas.get()}")
    if var_requisitos.get():
        print("Requisitos seleccionados")
        return "requisitos"
    elif var_documentos.get():
        print("Documentos seleccionados")
        return "documentos"
    elif var_proyectos.get():
        print("Proyectos seleccionados")
        return "proyectos"
    elif var_subsistemas.get():
        print("Subsistemas seleccionados")
        return "subsistemas"
    else:
        print("Ninguna opcion")
        return""

# Función para realizar la consulta y mostrar los resultados
def realizar_consulta(tipo_consulta, entry_subsistemas, entry_proyectos, entry_documentos,frame_visual):
    limpiar_visualizador(frame_visual) #limpiamos visualizador
    subsistema = entry_subsistemas.get()
    proyecto = entry_proyectos.get()
    documento = entry_proyectos.get()
        
    if tipo_consulta== "documentos":
        if subsistema or proyecto:
            documentos = obtener_documentos_filtrados(subsistema, proyecto, documento)
        else:
            documentos = obtener_documentos() 
            mostrar_resultados(documentos,frame_visual)
    
    elif tipo_consulta == "subsistemas":
        subsistemas = obtener_subsistemas()
        mostrar_resultados(subsistemas,frame_visual)
    
    elif tipo_consulta == "requisitos":
        requisitos = obtener_requisitos()
        mostrar_resultados(requisitos,frame_visual)
    
    elif tipo_consulta == "proyectos":
        requisitos = obtener_ciudades()
        mostrar_resultados(requisitos,frame_visual)

    else:
        messagebox.showerror("Error","Debe seleccionar un tipo de consulta")


def mostrar_resultados(resultados, frame_visual):

    limpiar_visualizador(frame_visual)  # Limpiamos el visualizador de resultados previos

    # Crear un Canvas y un Frame dentro de un Scrollbar para los resultados
    canvas = tk.Canvas(frame_visual)
    scrollbar = tk.Scrollbar(frame_visual, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Si no hay resultados, mostramos un mensaje
    if not resultados:
        label_vacio = tk.Label(scrollable_frame, text="No se encontraron resultados.")
        label_vacio.pack(pady=5)
        return

    # Configuramos el uso del grid en el frame visual
    for i, nombre_columna in enumerate(resultados[0]):
        label_encabezado = tk.Label(scrollable_frame, text=nombre_columna, font=("Arial", 10, "bold"), anchor="w", bg="lightgray", padx=5, pady=5)
        label_encabezado.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)

    # Asignamos el peso de las columnas para que se distribuyan uniformemente
    for i in range(len(resultados[0])):
        scrollable_frame.grid_columnconfigure(i, weight=1, uniform="columna")

    # Mostrar los datos
    for fila_index, fila in enumerate(resultados[1:], start=1):  # Empezamos desde la segunda fila (los datos)
        for col_index, dato in enumerate(fila):
            label_dato = tk.Label(scrollable_frame, text=str(dato), anchor="w", padx=5, pady=5, wraplength=210)  # wraplength ajustado
            label_dato.grid(row=fila_index, column=col_index, sticky="nsew", padx=5, pady=5)

    # Forzar redimensionamiento equitativo
    scrollable_frame.update_idletasks()

