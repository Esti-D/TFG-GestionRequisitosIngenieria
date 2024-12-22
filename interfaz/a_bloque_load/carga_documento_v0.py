import logging
import tkinter as tk
from tkinter import messagebox
import re
import os
import shutil
import fitz
from extraccion.leer_pdf import extraer_contenido_pdf, extraer_texto_pdf
from almacenamiento.func_documentos import insertar_documento, obtener_iddocumento
from almacenamiento.func_requisitos import insertar_requisito
from interfaz.c_bloque_acciones_independientes.bloque_asignaciones import (
    limpiar_visualizador,
)
from .asignar_subsistemas import asignar_subsistemas_a_documento_y_mostrar_ventana
from collections import Counter

def detectar_capitulos(contenido_pdf):
    # Dividir el contenido en fragmentos basados en capítulos 
    capitulos_detectados = re.split(r"(?=\d+\.\s)", contenido_pdf)
    return capitulos_detectados 

### version 2 CARGAR DOCUMETNO COMPLETOV2 ---------------------

import fitz
import re
from collections import Counter

import re
import fitz  # PyMuPDF

def detectar_estructura_capitulos_pdf(ruta_pdf, max_paginas=5):
    """
    Detecta automáticamente el patrón de capítulos en un PDF analizando las primeras páginas.

    Args:
        ruta_pdf (str): Ruta al archivo PDF.
        max_paginas (int): Número máximo de páginas a analizar.

    Returns:
        str: Patrón regex detectado para capítulos.
    """
    lineas_candidatas = []

    try:
        # Leer las primeras páginas del PDF
        with fitz.open(ruta_pdf) as pdf_document:
            for num_pagina, pagina in enumerate(pdf_document, start=1):
                if num_pagina > max_paginas:
                    break  # Analizar solo las primeras `max_paginas`

                texto_pagina = pagina.get_text("text")
                lineas_candidatas.extend(texto_pagina.splitlines())  # Dividir en líneas

    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
        return r"(?=\d+\.\s)"  # Retorno por defecto si hay un error

    # Patrones comunes de capítulos
    patrones_posibles = [
        r"\d+\.\s",          # Ejemplo: "1. Introduction"
        r"\d+\s",            # Ejemplo: "1 Introduction"
        r"\d+-\s",           # Ejemplo: "1- Introduction"
        r"\d+\)\s",          # Ejemplo: "1) Introduction"
        r"[IVXLCDM]+\.\s",   # Ejemplo: "I. Introduction" (números romanos) no funciona lo eliminamos 
    ]
    frecuencias = {patron: 0 for patron in patrones_posibles}

    # Contar las coincidencias de cada patrón en las líneas candidatas
    for linea in lineas_candidatas:
        for patron in patrones_posibles:
            if re.match(patron, linea.strip()):  # Verificar coincidencia
                frecuencias[patron] += 1

    # Mostrar las frecuencias de patrones detectadas (para depuración)
    print("Frecuencias de patrones detectadas:")
    for patron, frecuencia in frecuencias.items():
        print(f"{patron}: {frecuencia}")

    # Seleccionar el patrón más frecuente
    patron_detectado = max(frecuencias, key=frecuencias.get)

    if frecuencias[patron_detectado] == 0:
        # Si no se detecta ningún patrón, usar un patrón por defecto
        return r"(?=\d+\.\s)"
    
    #patron_detectado= r"(?=\d+\.\s)"
    concat= r"(?="
    patron_devuelto= f"{concat}{patron_detectado})"
    print(f"Patrón detectado: {patron_devuelto}")
    return patron_devuelto

def convertir_patron_capitulo(patron_estructura):
    """
    Convierte un patrón de prefijo en un patrón que capture el número y el texto del capítulo.

    Args:
        patron_estructura (str): Patrón base, como (?=\d+\.\s).

    Returns:
        str: Patrón transformado, como ^(\d+)\.\s+(.+).
    """
    # Elimina el `(?=` y el `)` para quedarnos con el núcleo del patrón
    base_patron = patron_estructura.replace("?=", "").replace("d+", "d+)").replace("s)", "s")
    #base_patron = patron_estructura.replace("(?=", "").replace("+","+)").replace("s)", "s")
    # Construye el patrón completo
    patron_completo = rf"^{base_patron}+(.+)"
    print(patron_completo)
    return patron_completo


def cargar_documento_completo(traducciones, entry_archivo, proyecto_id, frame_visual):
    """
    Extrae el contenido de un archivo PDF, organiza en capítulos según una estructura predefinida,
    y divide los requisitos, incluyendo imágenes y tablas.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        entry_archivo (tk.Entry): Campo de texto donde se muestra la ruta del archivo seleccionado.
        proyecto_id (int): ID del proyecto asociado al documento.
        frame_visual (tk.Frame): Frame donde se mostrarán los capítulos y requisitos extraídos.
    """
   
    """
    Extrae el contenido de un archivo PDF, organiza en capítulos, y divide los requisitos, incluyendo imágenes y tablas.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        entry_archivo (tk.Entry): Campo de texto donde se muestra la ruta del archivo seleccionado.
        proyecto_id (int): ID del proyecto asociado al documento.
        frame_visual (tk.Frame): Frame donde se mostrarán los capítulos y requisitos extraídos.
    """
    ruta_archivo = (
        entry_archivo.get()
    )  # Obtener la ruta del archivo del campo de entrada.
    titulo_documento = ruta_archivo.split("/")[
        -1
    ]  # Obtener solo el nombre del archivo.

    if not ruta_archivo:
        # Mostrar mensaje de error si no se seleccionó un archivo.
        messagebox.showerror(
            traducciones["M_Error"],
            traducciones["M_No_se_ha_seleccionado_ningún_archivo"],
        )
        return

    try:
        # Intentar extraer el texto del PDF.
        texto_pdf = extraer_contenido_pdf(ruta_archivo, "almacen/temporal", proyecto_id)
        if not texto_pdf:
            # Mostrar mensaje de error si no se pudo extraer texto.
            messagebox.showerror(
                traducciones["M_Error"],
                traducciones["M_No_se_pudo_extraer_texto_del_PDF"]
            )
            return

        
        # Limpiar cualquier contenido previo del frame de visualización.
        limpiar_visualizador(frame_visual)
        estructura= detectar_estructura_capitulos_pdf(ruta_archivo)
        # Dividir el texto en capítulos utilizando una expresión regular.
        capitulos = re.split(estructura, texto_pdf)
        lista_req_cap = []  # Lista para almacenar los capítulos y requisitos extraídos.
        contenido = ""  # Contenido a mostrar en el área de texto.

        for capitulo in capitulos:
            capitulo = capitulo.strip()  # Eliminar espacios en blanco.
            if not capitulo:
                continue
            
            patron_completo=convertir_patron_capitulo(estructura)
            # Buscar el número y título del capítulo con una expresión regular.
            #match_capitulo = re.match(r"^(\d+)\.\s+(.+)", capitulo, re.DOTALL)
            match_capitulo = re.match(patron_completo, capitulo, re.DOTALL)
            if match_capitulo:
                capitulo_actual = match_capitulo.group(1)  # Número del capítulo.
                texto_capitulo = match_capitulo.group(2)  # Texto del capítulo.

                contenido += f"{traducciones['T_CAPITULO']} {capitulo_actual} :\n"

                # Dividir el texto del capítulo en requisitos, basados en puntos y aparte.
                requisitos = re.split(r"(?<=\.)\s*\n(?=[A-Z])", texto_capitulo)
                id_requisito = 1

                for requisito in requisitos:
                    if requisito.strip():
                        texto_requisito = requisito.strip()  # Eliminar espacios.
                        lista_req_cap.append((capitulo_actual, texto_requisito))
                        contenido += f"{traducciones['T_REQUISITO']} {id_requisito}: {texto_requisito}\n"
                        id_requisito += 1

            contenido += "\n"

        # Mostrar el contenido extraído en un widget de texto dentro del frame.
        if contenido:
            texto_requisitos_visualizador = tk.Text(
                frame_visual, wrap="word", height=20
            )
            texto_requisitos_visualizador.insert(tk.END, contenido)
            texto_requisitos_visualizador.pack(
                pady=10, padx=10, fill="both", expand=True
            )
        else:
            # Mostrar mensaje de error si no se encontraron capítulos ni requisitos.
            messagebox.showerror(
                traducciones["M_Error"],
                traducciones[
                    "M_No_se_pudo_encontrar_ningún_capítulo_o_requisito_en_el_documento"
                ],
            )

        # Crear un botón para guardar los datos extraídos.
        boton_guardar = tk.Button(
            frame_visual,
            text=traducciones["B_GUARDAR"],
            command=lambda: guardar_requisitos_completos_y_asociaciones(
                traducciones,
                titulo_documento,
                lista_req_cap,
                texto_requisitos_visualizador.get("1.0", tk.END),
                ruta_archivo,
                proyecto_id,
                frame_visual,
            ),
        )
        boton_guardar.pack(pady=10)

    except Exception as e:
        # Capturar y mostrar errores inesperados.
        print(f"{traducciones['M_Error_al_cargar_el_documento']} {e}")
        messagebox.showerror(
            traducciones["M_Error"],
            f"{traducciones['M_Error_al_cargar_el_documento']} {e}",
        )

















### version 1 CARGAR DOCUMETNO COMPLETOV1 ---------------------
def detectar_capitulos(contenido_pdf):
    # Dividir el contenido en fragmentos basados en capítulos 
    capitulos_detectados = re.split(r"(?=\d+\.\s)", contenido_pdf)
    return capitulos_detectados


def cargar_documento_completo_v1 (traducciones, entry_archivo, proyecto_id, frame_visual):

    """
    Extrae el contenido de un archivo PDF, organiza en capítulos, y divide los requisitos, incluyendo imágenes y tablas.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        entry_archivo (tk.Entry): Campo de texto donde se muestra la ruta del archivo seleccionado.
        proyecto_id (int): ID del proyecto asociado al documento.
        frame_visual (tk.Frame): Frame donde se mostrarán los capítulos y requisitos extraídos.
    """
    ruta_archivo = (
        entry_archivo.get()
    )  # Obtener la ruta del archivo del campo de entrada.
    titulo_documento = ruta_archivo.split("/")[
        -1
    ]  # Obtener solo el nombre del archivo.

    if not ruta_archivo:
        # Mostrar mensaje de error si no se seleccionó un archivo.
        messagebox.showerror(
            traducciones["M_Error"],
            traducciones["M_No_se_ha_seleccionado_ningún_archivo"],
        )
        return

    try:
        # Intentar extraer el texto del PDF.
        texto_pdf = extraer_contenido_pdf(ruta_archivo, "almacen/temporal", proyecto_id)
        if not texto_pdf:
            # Mostrar mensaje de error si no se pudo extraer texto.
            messagebox.showerror(
                traducciones["M_Error"],
                traducciones["M_No_se_pudo_extraer_texto_del_PDF"]
            )
            return

        
        # Limpiar cualquier contenido previo del frame de visualización.
        limpiar_visualizador(frame_visual)

        # Dividir el texto en capítulos utilizando una expresión regular.
        capitulos = detectar_capitulos(texto_pdf)
        lista_req_cap = []  # Lista para almacenar los capítulos y requisitos extraídos.
        contenido = ""  # Contenido a mostrar en el área de texto.

        for capitulo in capitulos:
            capitulo = capitulo.strip()  # Eliminar espacios en blanco.
            if not capitulo:
                continue

            # Buscar el número y título del capítulo con una expresión regular.
            match_capitulo = re.match(r"^(\d+)\.\s+(.+)", capitulo, re.DOTALL)
            if match_capitulo:
                capitulo_actual = match_capitulo.group(1)  # Número del capítulo.
                texto_capitulo = match_capitulo.group(2)  # Texto del capítulo.

                contenido += f"{traducciones['T_CAPITULO']} {capitulo_actual} :\n"

                # Dividir el texto del capítulo en requisitos, basados en puntos y aparte.
                requisitos = re.split(r"(?<=\.)\s*\n(?=[A-Z])", texto_capitulo)
                id_requisito = 1

                for requisito in requisitos:
                    if requisito.strip():
                        texto_requisito = requisito.strip()  # Eliminar espacios.
                        lista_req_cap.append((capitulo_actual, texto_requisito))
                        contenido += f"{traducciones['T_REQUISITO']} {id_requisito}: {texto_requisito}\n"
                        id_requisito += 1

            contenido += "\n"

        # Mostrar el contenido extraído en un widget de texto dentro del frame.
        if contenido:
            texto_requisitos_visualizador = tk.Text(
                frame_visual, wrap="word", height=20
            )
            texto_requisitos_visualizador.insert(tk.END, contenido)
            texto_requisitos_visualizador.pack(
                pady=10, padx=10, fill="both", expand=True
            )
        else:
            # Mostrar mensaje de error si no se encontraron capítulos ni requisitos.
            messagebox.showerror(
                traducciones["M_Error"],
                traducciones[
                    "M_No_se_pudo_encontrar_ningún_capítulo_o_requisito_en_el_documento"
                ],
            )

        # Crear un botón para guardar los datos extraídos.
        boton_guardar = tk.Button(
            frame_visual,
            text=traducciones["B_GUARDAR"],
            command=lambda: guardar_requisitos_completos_y_asociaciones(
                traducciones,
                titulo_documento,
                lista_req_cap,
                texto_requisitos_visualizador.get("1.0", tk.END),
                ruta_archivo,
                proyecto_id,
                frame_visual,
            ),
        )
        boton_guardar.pack(pady=10)

    except Exception as e:
        # Capturar y mostrar errores inesperados.
        print(f"{traducciones['M_Error_al_cargar_el_documento']} {e}")
        messagebox.showerror(
            traducciones["M_Error"],
            f"{traducciones['M_Error_al_cargar_el_documento']} {e}",
        )



def guardar_requisitos_completos_y_asociaciones(
    traducciones,
    titulo_documento,
    lista_req_cap,
    requisitos_editados,
    ruta_archivo,
    proyecto_id,
    frame_visual,
):
    """
    Guarda el documento y los requisitos extraídos en la base de datos, 
    y luego asigna subsistemas sugeridos, incluyendo el manejo de imágenes y tablas.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        titulo_documento (str): Título del documento procesado.
        lista_req_cap (list): Lista de tuplas (capítulo, contenido, tipo) extraídas del documento.
        requisitos_editados (str): Texto de los requisitos tras posibles ediciones.
        ruta_archivo (str): Ruta del archivo procesado.
        proyecto_id (int): ID del proyecto asociado al documento.
        frame_visual (tk.Frame): Frame para la visualización de resultados.

    Flujo:
        1. Guarda el documento en la base de datos.
        2. Inserta los requisitos asociados al documento y sus capítulos.
        3. Renombra y mueve las tablas e imágenes de la carpeta temporal a la permanente.
        4. Asigna subsistemas sugeridos al documento guardado.
    """

    try:
        # 1. Insertar el documento en la base de datos.
        insertar_documento(titulo_documento, "1.0", proyecto_id)
        documento_id = obtener_iddocumento(titulo_documento, proyecto_id)

        # 2. Procesar y guardar los requisitos.
        for capitulo, texto_requisito in lista_req_cap:
            insertar_requisito(capitulo, texto_requisito, documento_id)


        # 3. Renombrar y mover tablas e imágenes.
        mover_archivos_desde_temporal(documento_id)

        # 4. Mostrar mensaje de éxito tras guardar los datos.
        messagebox.showinfo(
            traducciones["M_Exito"],
            traducciones[
                "M_Documentos,requisitos_y_asociaciones_guardados_correctamente"
            ],
        )

        # 5. Llamar a la función para asignar subsistemas sugeridos.
        asignar_subsistemas_a_documento_y_mostrar_ventana(
            traducciones, requisitos_editados, documento_id, frame_visual
        )

    except Exception as e:
        # Mostrar un mensaje de error si ocurre algún problema al guardar.
        messagebox.showerror(
            traducciones["M_Error"],
            f"{traducciones['M_Error_al_guardar_los_requisitos']}{e}",
        )


def mover_archivos_desde_temporal(documento_id):
    """
    Mueve los archivos gráficos desde la carpeta temporal a su ubicación definitiva.

    Args:
        documento_id (int): ID del documento asociado.
        proyecto_id (int): ID del proyecto asociado.
    """
    temporal_path = "almacen/temporal/"
    permanente_path = "almacen/permanente/"

    # Verificar que ambas carpetas existan
    if not os.path.exists(temporal_path):
        print(f"La carpeta temporal no existe: {temporal_path}")
        return

    if not os.path.exists(permanente_path):
        os.makedirs(permanente_path)

    # Procesar los archivos en la carpeta temporal
    for archivo in os.listdir(temporal_path):
        # Separar nombre y extensión
        nombre, ext = os.path.splitext(archivo)
        # Validar el tipo de archivo (CSV para tablas, PNG para imágenes)
        if ext.lower() in [".csv", ".jpeg"]:
            tipo = "tabla" if ext.lower() == ".csv" else "imagen"
            nuevo_nombre = f"{nombre}D{documento_id:02}{ext}"
            archivo_origen = os.path.join(temporal_path, archivo)
            archivo_destino = os.path.join(permanente_path, nuevo_nombre)

            # Mover el archivo
            shutil.move(archivo_origen, archivo_destino)
            print(f"Archivo movido: {archivo_origen} -> {archivo_destino}")


