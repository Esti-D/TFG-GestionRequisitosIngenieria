import tkinter as tk
from tkinter import messagebox
from almacenamiento.func_documentos import (
    obtener_documentos,
    obtener_documentos_filtrados,
    obtener_iddocumento,
)  # función de consulta de documentos
from almacenamiento.func_subsistemas import (
    obtener_id_subsistema,
    obtener_subsistemas_filtrados,
    obtener_subsistemas,
)  # funcion de consulta de subssistemas
from almacenamiento.func_requisitos import (
    obtener_requisitos,
    obtener_requisitos_filtrados,
)  # funcion de consulta de requisitos
from almacenamiento.func_proyectos import (
    obtener_id_proyecto,
    obtener_proyectos_filtrados,
    obtener_proyectos,
)  # funcion de consulta de proyectos


# Función para limpiar el contenido del visualizador (por si es necesario en alguna funcionalidad)
def limpiar_visualizador(frame_visual):
    for widget in frame_visual.winfo_children():
        widget.destroy()


# funcion para verificar que opcion se ha escogido para realizar la consulta
def verificar_opcion_seleccionada(
    traducciones, var_requisitos, var_documentos, var_proyectos, var_subsistemas
):

    print(
        f"{traducciones["C_Requisitos"]}:{var_requisitos.get()},{traducciones["C_Documentos"]}: {var_documentos.get()},{traducciones["C_Proyectos"]}: {var_proyectos.get()},{traducciones["C_Subsistemas"]}:{var_subsistemas.get()}"
    )
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
        return ""


# Función para realizar la consulta y mostrar los resultados
def realizar_consulta(
    traducciones,
    tipo_consulta,
    combobox_subsistemas,
    combobox_proyectos,
    combobox_documentos,
    frame_visual,
):
    limpiar_visualizador(frame_visual)  # limpiamos visualizador
    subsistema = combobox_subsistemas.get()
    proyecto = combobox_proyectos.get()
    documento = combobox_documentos.get()

    # limpieza de filtros
    if proyecto == traducciones["O_TODOS"]:
        proyecto = None
    if subsistema == traducciones["O_TODOS"]:
        subsistema = None
    if documento == traducciones["O_TODOS"]:
        documento = None

    print(f"Proyecto seleccionado: {proyecto}")
    print(f"Documento seleccionado: {documento}")
    print(f"Subsistema seleccionado: {subsistema}")

    if tipo_consulta == "requisitos":
        if subsistema or proyecto or documento:
            subsistemaid = obtener_id_subsistema(subsistema)
            proyectoid = obtener_id_proyecto(proyecto)
            documentoid = obtener_iddocumento(documento, proyectoid)

            requisitos = obtener_requisitos_filtrados(
                subsistemaid, proyectoid, documentoid
            )
        else:
            requisitos = obtener_requisitos()

        mostrar_resultados(
            traducciones, requisitos, frame_visual, tipo_datos="requisitos"
        )

    elif tipo_consulta == "documentos":
        if subsistema or proyecto or documento:
            documentos = obtener_documentos_filtrados(subsistema, proyecto, documento)
            print(f"Proyecto seleccionado: {proyecto}")
            print(f"Documento seleccionado: {documento}")
            print(f"Subsistema seleccionado: {subsistema}")
        else:
            documentos = obtener_documentos()
        mostrar_resultados(
            traducciones, documentos, frame_visual, tipo_datos="documentos"
        )

    elif tipo_consulta == "proyectos":
        if documento or subsistema:
            subsistemaid = obtener_id_subsistema(subsistema)
            proyectoid = obtener_id_proyecto(proyecto)
            documentoid = obtener_iddocumento(documento, proyectoid)
            proyectos = obtener_proyectos_filtrados(
                subsistemaid, proyectoid, documentoid
            )

        else:
            proyectos = obtener_proyectos()
        mostrar_resultados(traducciones, proyectos, frame_visual, tipo_datos="general")

    elif tipo_consulta == "subsistemas":
        if proyecto or documento:
            subsistemaid = obtener_id_subsistema(subsistema)
            proyectoid = obtener_id_proyecto(proyecto)
            documentoid = obtener_iddocumento(documento, proyectoid)
            subsistemas = obtener_subsistemas_filtrados(
                subsistemaid, proyectoid, documentoid
            )

        else:
            subsistemas = obtener_subsistemas()
        mostrar_resultados(
            traducciones, subsistemas, frame_visual, tipo_datos="general"
        )

    else:
        messagebox.showerror(
            traducciones["M_Error"],
            traducciones["M_Debe_seleccionar_un_tipo_de_consulta"],
        )


def mostrar_resultados(traducciones, resultados, frame_visual, tipo_datos="general"):

    limpiar_visualizador(
        frame_visual
    )  # Limpiamos el visualizador de resultados previos

    # Crear un Canvas y un Frame dentro de un Scrollbar para los resultados
    canvas = tk.Canvas(frame_visual)
    scrollbar = tk.Scrollbar(frame_visual, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Si no hay resultados, mostramos un mensaje
    if not resultados:
        label_vacio = tk.Label(
            scrollable_frame, traducciones["M_No_se_encontraron_resultados"]
        )
        label_vacio.pack(pady=5)
        return

    # Asignamos el peso de las columnas para que se distribuyan según el tipo de datos
    for i in range(len(resultados[0])):
        if (
            tipo_datos == "documentos" and i == 2
        ):  # Si es documentos, expande la columna 2
            scrollable_frame.grid_columnconfigure(i, weight=3, minsize=150)
        elif (
            tipo_datos == "requisitos" and i == 3
        ):  # Si es requisitos, expande la columna 3
            scrollable_frame.grid_columnconfigure(i, weight=3, minsize=150)
        else:
            scrollable_frame.grid_columnconfigure(
                i, weight=1, minsize=100
            )  # Otras columnas

    # Configuramos el uso del grid en el frame visual
    for i, nombre_columna in enumerate(resultados[0]):
        label_encabezado = tk.Label(
            scrollable_frame,
            text=nombre_columna,
            font=("Arial", 10, "bold"),
            anchor="w",
            bg="lightgray",
            padx=5,
            pady=5,
        )
        label_encabezado.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)

    # Mostrar los datos
    for fila_index, fila in enumerate(
        resultados[1:], start=1
    ):  # Empezamos desde la segunda fila (los datos)
        for col_index, dato in enumerate(fila):
            label_dato = tk.Label(
                scrollable_frame,
                text=str(dato),
                anchor="w",
                padx=5,
                pady=5,
                wraplength=800,
            )  # wraplength ajustado
            label_dato.grid(
                row=fila_index, column=col_index, sticky="nsew", padx=5, pady=5
            )

    # Forzar redimensionamiento equitativo
    scrollable_frame.update_idletasks()
