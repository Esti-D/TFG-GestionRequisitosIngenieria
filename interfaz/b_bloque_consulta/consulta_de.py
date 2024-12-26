"""
Archivo: consulta_de.py
Descripción: Este archivo contiene funciones para gestionar las consultas de
datos en la aplicación. Permite realizar consultas basadas en filtros y mostrar
resultados en la interfaz gráfica, así como gestionar la visualización y 
eliminación de archivos relacionados.

Autor: Estíbalitz Díez
Fecha: 26/12/2024
Versión: 2
"""

import tkinter as tk
import os
from tkinter import messagebox
from almacenamiento.func_documentos import (
    borrar_documento,
    obtener_documentos,
    obtener_documentos_filtrados,
    obtener_iddocumento,
    obtener_version,
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
    """
    Elimina todos los widgets dentro del frame_visual.

    Args:
        frame_visual (tk.Frame): Frame que será limpiado.
    """
    for widget in frame_visual.winfo_children():
        widget.destroy()


# funcion para verificar que opcion se ha escogido para realizar la consulta
def verificar_opcion_seleccionada(
    traducciones,
    var_requisitos,
    var_documentos,
    var_proyectos,
    var_subsistemas,
    var_tab_ima,
):
    """
    Verifica cuál opción de consulta ha sido seleccionada por el usuario.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        var_requisitos (tk.BooleanVar): Variable asociada a la selección de requisitos.
        var_documentos (tk.BooleanVar): Variable asociada a la selección de documentos.
        var_proyectos (tk.BooleanVar): Variable asociada a la selección de proyectos.
        var_subsistemas (tk.BooleanVar): Variable asociada a la selección de subsistemas.
        var_tab_ima (tk.BooleanVar): Variable asociada a la selección de tablas/imagenes.

    Returns:
        str: Tipo de consulta seleccionada, o una cadena vacía si no se seleccionó nada.
    """
    print(
        f"{traducciones["C_Requisitos"]}:{var_requisitos.get()},"
        f"{traducciones["C_Documentos"]}: {var_documentos.get()},"
        F"{traducciones["C_Proyectos"]}: {var_proyectos.get()},"
        f"{traducciones["C_Subsistemas"]}:{var_subsistemas.get()}"
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
    elif var_tab_ima.get():
        print("R. Tablas_Figuras seleccionados")
        return "r_tab_ima"
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
    """
    Realiza la consulta según el tipo seleccionado y muestra los resultados en el
    frame_visual.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        tipo_consulta (str): Tipo de consulta a realizar (requisitos, documentos, proyectos,
        subsistemas, r_tab_ima).
        combobox_subsistemas (ttk.Combobox): Combobox con el filtro de subsistemas.
        combobox_proyectos (ttk.Combobox): Combobox con el filtro de proyectos.
        combobox_documentos (ttk.Combobox): Combobox con el filtro de documentos.
        frame_visual (tk.Frame): Frame donde se mostrarán los resultados.
    """
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
            documentoid = obtener_iddocumento(
                documento, proyectoid, obtener_version(documento, proyectoid)
            )

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
            documentoid = obtener_iddocumento(
                documento, proyectoid, obtener_version(documento, proyectoid)
            )
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
            documentoid = obtener_iddocumento(
                documento, proyectoid, obtener_version(documento, proyectoid)
            )
            subsistemas = obtener_subsistemas_filtrados(
                subsistemaid, proyectoid, documentoid
            )

        else:
            subsistemas = obtener_subsistemas()
        mostrar_resultados(
            traducciones, subsistemas, frame_visual, tipo_datos="general"
        )
    elif tipo_consulta == "r_tab_ima":
        if proyecto or documento:
            proyectoid = obtener_id_proyecto(proyecto)
            documentoid = obtener_iddocumento(
                documento, proyectoid, obtener_version(documento, proyectoid)
            )
            mostrar_archivos(frame_visual, traducciones, proyectoid, documentoid)
        else:
            mostrar_archivos(frame_visual, traducciones, None, None)

    else:
        messagebox.showerror(
            traducciones["M_Error"],
            traducciones["M_Debe_seleccionar_un_tipo_de_consulta"],
        )


def mostrar_archivos(frame_visual, traducciones, proyectoid=None, documentoid=None):
    """
    Muestra los archivos filtrados en la interfaz con opciones de visualización y eliminación.

    Args:
        frame_visual (tk.Frame): Frame donde se mostrarán los archivos.
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        proyectoid (int, opcional): ID del proyecto para filtrar los archivos. Por defecto, None.
        documentoid (int, opcional): ID del documento para filtrar los archivos. Por defecto, None.
    """
    limpiar_visualizador(
        frame_visual
    )  # Limpiamos el visualizador de resultados previos

    # Ruta de la carpeta 'almacen/permanente'
    ruta_permanente = os.path.join(os.getcwd(), "almacen", "permanente")
    archivos = os.listdir(ruta_permanente)

    # Mostrar cada archivo con un botón de visualización
    archivos_filtrados = []
    for archivo in archivos:
        if not archivo.lower().endswith((".jpeg", ".jpg", ".png", ".csv")):
            continue

        # Filtro por proyecto (buscar P<num>)
        if proyectoid and f"P0{proyectoid}" not in archivo:
            continue

        # Filtro por documento (buscar D<num>)
        if documentoid and f"D0{documentoid}" not in archivo:
            continue

        # Agregar archivo que cumple con los filtros
        archivos_filtrados.append(archivo)

    # Mostrar los archivos filtrados o todos si no hay filtros
    for archivo in archivos_filtrados:

        frame_item = tk.Frame(frame_visual, bg="white", pady=5)
        frame_item.pack(fill="x")

        label_archivo = tk.Label(frame_item, text=archivo, bg="white")
        label_archivo.pack(side="left", padx=10)

        boton_visualizar = tk.Button(
            frame_item,
            text=traducciones["B_VER"],
            command=lambda archivo=archivo: abrir_archivo(ruta_permanente, archivo),
            bg="#125ca6",
            fg="white",
            width=3,
        )
        boton_visualizar.pack(side="right", padx=10)

        # Botón Eliminar
        boton_eliminar = tk.Button(
            frame_item,
            text=traducciones["B_ELIMINAR"],
            command=lambda archivo=archivo: eliminar_archivo(
                traducciones, ruta_permanente, archivo, frame_item
            ),
            bg="red",
            fg="white",
            width=7,
        )
        boton_eliminar.pack(side="right", padx=5)


def eliminar_archivo(traducciones, ruta_permanente, archivo, frame_item):
    """
    Elimina un archivo de la carpeta 'almacen/permanente' tras confirmación del usuario.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        ruta_permanente (str): Ruta base donde se encuentran los archivos.
        archivo (str): Nombre del archivo que se desea eliminar.
        frame_item (tk.Frame): Frame asociado al archivo en la interfaz, que será 
        eliminado visualmente.

    Funcionalidad:
        - Solicita confirmación al usuario antes de eliminar el archivo.
        - Elimina el archivo físicamente del sistema si el usuario confirma.
        - Actualiza la interfaz eliminando el frame visual del archivo.
    """
    respuesta = messagebox.askyesno(
        traducciones["M_Confirmar_Eliminacion"],
        traducciones["M_Confirmar_Eliminacion_T"].format(archivo=archivo),
    )

    if respuesta:
        ruta_completa = os.path.join(ruta_permanente, archivo)
        try:
            os.remove(ruta_completa)  # Eliminar el archivo
            frame_item.destroy()  # Quitar el elemento visual
            messagebox.showinfo(
                traducciones["M_Archivo_Eliminado"], traducciones["M_Archivo_Eliminado"]
            )
        except Exception as e:
            messagebox.showerror(
                traducciones["M_Error"], traducciones["M_Error"].format(archivo=archivo)
            )


def abrir_archivo(ruta_permanente, archivo):
    """
    Abre una ventana para visualizar el contenido de un archivo.

    Args:
        ruta_permanente (str): Ruta base donde se encuentran los archivos.
        archivo (str): Nombre del archivo que se desea visualizar.

    Funcionalidad:
        - Visualiza imágenes en formatos soportados (.jpeg, .jpg, .png).
        - Muestra el contenido de archivos CSV.
        - Muestra un mensaje para tipos de archivo no soportados.
    """
    ruta_completa = os.path.join(ruta_permanente, archivo)

    # Crear una nueva ventana
    ventana = tk.Toplevel()
    ventana.title(f"Visualizando {archivo}")

    # Mostrar imágenes
    if archivo.lower().endswith((".jpeg", ".jpg", ".png")):
        from PIL import Image, ImageTk

        imagen = Image.open(ruta_completa)
        imagen_tk = ImageTk.PhotoImage(imagen)

        label_imagen = tk.Label(ventana, image=imagen_tk)
        label_imagen.image = imagen_tk  # Necesario para mantener la referencia
        label_imagen.pack()

    # Mostrar tablas (CSV)
    elif archivo.lower().endswith(".csv"):
        import csv

        with open(ruta_completa, newline="", encoding="utf-8") as csvfile:
            lector = csv.reader(csvfile)
            text_area = tk.Text(ventana, wrap="none", width=80, height=20)
            text_area.pack(fill="both", expand=True)

            for fila in lector:
                text_area.insert(tk.END, ", ".join(fila) + "\n")
    else:
        tk.Label(ventana, text="Tipo de archivo no soportado").pack()


def mostrar_resultados(traducciones, resultados, frame_visual, tipo_datos="general"):
    """
    Muestra los resultados de una consulta en un frame con scroll.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        resultados (list): Lista de resultados a mostrar, donde la primera fila contiene los
        encabezados.
        frame_visual (tk.Frame): Frame donde se mostrarán los resultados.
        tipo_datos (str): Tipo de datos a mostrar (ej. "requisitos", "documentos", "general").

    """
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

    # Traducir los encabezados según el idioma actual
    encabezados_traducidos = [
        traducciones.get(col, col) for col in resultados[0]
    ]  # Traducir cada encabezado

    # Mostrar encabezados traducidos
    for i, nombre_columna in enumerate(encabezados_traducidos):
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

        # Boton Eliminar
        btn_eliminar = tk.Button(
            scrollable_frame,
            text=traducciones["B_ELIMINAR"],
            command=lambda doc_id=fila[0]: borrar_documento(doc_id),
            bg="red",
            fg="white",
            padx=5,
            pady=5,
        )
        btn_eliminar.grid(
            row=fila_index, column=len(resultados[0]), sticky="nsew", padx=5, pady=5
        )
    # Forzar redimensionamiento equitativo
    scrollable_frame.update_idletasks()
