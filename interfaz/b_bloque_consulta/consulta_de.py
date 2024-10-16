import tkinter as tk
from tkinter import messagebox
from almacenamiento.func_documentos import obtener_documentos, obtener_iddocumento #función de consulta de documentos
from almacenamiento.func_subsistemas import obtener_id_subsistema, obtener_subsistemas #funcion de consulta de subssistemas
from almacenamiento.func_requisitos import obtener_requisitos # funcion de consulta de requisitos
from almacenamiento.func_proyectos import obtener_id_proyecto, obtener_proyectos # funcion de consulta de proyectos
from almacenamiento.func_documentos import obtener_documentos_filtrados #funcion de consulta de doc filtrados
from almacenamiento.func_subsistemas import obtener_subsistemas_filtrados #funcion de consulta de subsistemas filtrados
from almacenamiento.func_requisitos import obtener_requisitos_filtrados #funcin de ocnsulta requisitos fitlrados
from almacenamiento.func_proyectos import obtener_proyectos_filtrados 

# Función para limpiar el contenido del visualizador (por si es necesario en alguna funcionalidad)
def limpiar_visualizador(frame_visual):
    for widget in frame_visual.winfo_children():
        widget.destroy()


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
def realizar_consulta(tipo_consulta, combobox_subsistemas, combobox_proyectos, combobox_documentos,frame_visual):
    limpiar_visualizador(frame_visual) #limpiamos visualizador
    subsistema = combobox_subsistemas.get()
    proyecto = combobox_proyectos.get()
    documento = combobox_documentos.get()

    # Inicializar documentos y requisitos para evitar errores si no se inicializan en los bloques posteriores
    #documentos = []
    #requisitos = []
    #proyectos = []
    #subsistemas = []
    print(f"Proyecto seleccionado: {proyecto}")
    print(f"Documento seleccionado: {documento}")
    print(f"Subsistema seleccionado: {subsistema}")

    if tipo_consulta == "requisitos":
        if subsistema or proyecto or documento:
            subsistemaid = obtener_id_subsistema(subsistema)
            proyectoid = obtener_id_proyecto(proyecto)
            documentoid = obtener_iddocumento(documento,proyectoid)
            
            requisitos = obtener_requisitos_filtrados(subsistemaid, proyectoid, documentoid)
        else:
            requisitos = obtener_requisitos()
        mostrar_resultados(requisitos,frame_visual)

    elif tipo_consulta== "documentos":
        if subsistema or proyecto:
            documentos = obtener_documentos_filtrados(subsistema, proyecto, documento)
            print(f"Proyecto seleccionado: {proyecto}")
            print(f"Documento seleccionado: {documento}")
            print(f"Subsistema seleccionado: {subsistema}")
        else:
            documentos = obtener_documentos() 
        mostrar_resultados(documentos,frame_visual)
    
    elif tipo_consulta == "proyectos":
        if documento or subsistema:
            proyectos = obtener_proyectos_filtrados(subsistema, proyecto, documento)
        else:
            proyectos = obtener_proyectos()
        mostrar_resultados(proyectos,frame_visual) 

    elif tipo_consulta == "subsistemas":
        if proyecto or documento:
            subsistemas= obtener_subsistemas_filtrados(subsistema, proyecto, documento)
        else:
            subsistemas = obtener_subsistemas()
        mostrar_resultados(subsistemas,frame_visual)
   
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

