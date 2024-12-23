import logging
import tkinter as tk
from tkinter import messagebox
import re
import os
import shutil
import fitz  # PyMuPDF
from collections import Counter

from extraccion.leer_pdf import extraer_contenido_pdf, extraer_texto_pdf
from almacenamiento.func_documentos import insertar_documento, obtener_iddocumento, obtener_version
from almacenamiento.func_requisitos import insertar_requisito
from interfaz.c_bloque_acciones_independientes.bloque_asignaciones import (limpiar_visualizador,)
from interfaz.d_bloque_otros.ayuda.bloque_ayuda import abrir_ayuda
from .asignar_subsistemas import asignar_subsistemas_a_documento_y_mostrar_ventana


### version NUEVA ESTRUCTURA V2 ---------------------


def detectar_estructura_capitulos_pdf(traducciones, entry_archivo, proyecto_id, frame_visual):
    """
    Detecta automáticamente el patrón de capítulos en un PDF analizando las primeras páginas.

    Args:
        ruta_pdf (str): Ruta al archivo PDF.
        max_paginas (int): Número máximo de páginas a analizar.

    Returns:
        str: Patrón regex detectado para capítulos.
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
    
    max_paginas=5
    
    lineas_candidatas = []

    try:
        # Leer las primeras páginas del PDF
        with fitz.open(ruta_archivo) as pdf_document:
            for num_pagina, pagina in enumerate(pdf_document, start=1):
                if num_pagina > max_paginas:
                    break  # Analizar solo las primeras `max_paginas`

                texto_pagina = pagina.get_text("text")
                lineas_candidatas.extend(texto_pagina.splitlines())  # Dividir en líneas

    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
        return None # Retorno por defecto si hay un error

    # Patrones comunes de capítulos
    patrones_posibles = [
        r"\d+\.\s",          # Ejemplo: "1. Introduction"
        r"\d+\s",            # Ejemplo: "1 Introduction"
        r"\d+-\s",           # Ejemplo: "1- Introduction"
        r"\d+\)\s",          # Ejemplo: "1) Introduction"
        #r"[IVXLCDM]+\.\s",   # Ejemplo: "I. Introduction" (números romanos) no funciona lo eliminamos 
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
    concat= r"(?="
    patron_devuelto= f"{concat}{patron_detectado})"
    print(f"Patrón detectado: {patron_devuelto}")

    if frecuencias[patron_detectado] == 0:
               
            # Crear una ventana personalizada
            ventana_opciones = tk.Toplevel()
            ventana_opciones.title("Estructura_de_capitulos")
            
            # Configurar tamaño inicial y cargar icono
            ventana_opciones.geometry("300x150")
            ventana_opciones.iconbitmap("./logos/logo_reducido.ico")

            # Mensaje de aviso
            mensaje = tk.Label(
                ventana_opciones,text=traducciones["Estructura_de_capitulos_no_reconocida"],
                wraplength=350,
                justify="center",
            )
            mensaje.pack(pady=20)

            # Crear un frame para organizar los botones en una fila
            frame_botones = tk.Frame(ventana_opciones)
            frame_botones.pack(expand=True, pady=20)

            # Variable para almacenar la decisión del usuario
            decision = tk.StringVar()

            # Botón "Forzar"
            boton_forzar = tk.Button(
                frame_botones,
                text="Forzar",
                command=lambda:[ cargar_documento_completo_sin_capitulos(ruta_archivo, titulo_documento, traducciones, entry_archivo, proyecto_id, frame_visual),
                ventana_opciones.destroy(),] # Cierra la ventana emergente
            )
            boton_forzar.pack(side="left", padx=10)

            # Botón "Cancelar"
            boton_cancelar = tk.Button(
                frame_botones,
                text="Cancelar",
                command=lambda: ventana_opciones.destroy(),
            )
            boton_cancelar.pack(side="left", padx=10)

            # Botón "Modificar PDF"
            boton_modificar = tk.Button(
                frame_botones,
                text="Modificar PDF",
                command=lambda: [ventana_opciones.destroy(), abrir_ayuda(traducciones, frame_visual), ] # Cierra la ventana emergente
            )
            boton_modificar.pack(side="left", padx=10)

            ventana_opciones.transient()  # Modal
            ventana_opciones.grab_set()  # Bloquea interacción con otras ventanas
            ventana_opciones.wait_variable(decision)  # Esperar a que el usuario tome una decisión
            ventana_opciones.destroy()
            
    else:
        return cargar_documento_completo(ruta_archivo, patron_devuelto, titulo_documento, traducciones, entry_archivo, proyecto_id, frame_visual)

def convertir_patron_capitulo(patron_estructura):
    
    base_patron = patron_estructura.replace("?=", "").replace("d+", "d+)").replace("s)", "s")
    # Construye el patrón completo
    patron_completo = rf"^{base_patron}+(.+)"
    print(patron_completo)
    return patron_completo

def cargar_documento_completo_sin_capitulos(ruta_archivo, titulo_documento, traducciones, entry_archivo, proyecto_id, frame_visual):
    """
        Extrae el contenido de un archivo PDF, organiza en capítulos según una estructura predefinida,
        y divide los requisitos, incluyendo imágenes y tablas.

        Args:
            traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
            entry_archivo (tk.Entry): Campo de texto donde se muestra la ruta del archivo seleccionado.
            proyecto_id (int): ID del proyecto asociado al documento.
            frame_visual (tk.Frame): Frame donde se mostrarán los capítulos y requisitos extraídos.
        """
    

    try:
                
        # Limpiar cualquier contenido previo del frame de visualización.
        limpiar_visualizador(frame_visual)      

        # Intentar extraer el texto del PDF.
        texto_pdf = extraer_contenido_pdf(ruta_archivo, "almacen/temporal", proyecto_id)
                
        if not texto_pdf:
            # Mostrar mensaje de error si no se pudo extraer texto.
            messagebox.showerror(
                traducciones["M_Error"],
                traducciones["M_No_se_pudo_extraer_texto_del_PDF"]
            )
            return
        # Dividir el texto en capítulos utilizando una expresión regular.
        #capitulos = re.split(patron_devuelto, texto_pdf)
        lista_req_cap = []  # Lista para almacenar los capítulos y requisitos extraídos.
        contenido = ""  # Contenido a mostrar en el área de texto.

        #for capitulo in capitulos:
        #    capitulo = capitulo.strip()  # Eliminar espacios en blanco.
        #    if not capitulo:
        #        continue
                    
        #    patron_completo=convertir_patron_capitulo(patron_devuelto)
        #    # Buscar el número y título del capítulo con una expresión regular.
        #    match_capitulo = re.match(patron_completo, capitulo, re.DOTALL)
        #    if match_capitulo:
        #        capitulo_actual = match_capitulo.group(1)  # Número del capítulo.
        #        texto_capitulo = match_capitulo.group(2)  # Texto del capítulo.

        #        contenido += f"{traducciones['T_CAPITULO']} {capitulo_actual} :\n"

                # Dividir el texto del capítulo en requisitos, basados en puntos y aparte.
        requisitos = re.split(r"(?<=\.)\s*\n(?=[A-Z])", texto_pdf)
        id_requisito = 1

        for requisito in requisitos:
            if requisito.strip():
                texto_requisito = requisito.strip()  # Eliminar espacios.
                #lista_req_cap.append((capitulo_actual, texto_requisito))
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
                    command=lambda: verificacion_version(
                        traducciones,
                        titulo_documento,
                        lista_req_cap,
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

def cargar_documento_completo(ruta_archivo, patron_devuelto, titulo_documento, traducciones, entry_archivo, proyecto_id, frame_visual):
    """
    Extrae el contenido de un archivo PDF, organiza en capítulos según una estructura predefinida,
    y divide los requisitos, incluyendo imágenes y tablas.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        entry_archivo (tk.Entry): Campo de texto donde se muestra la ruta del archivo seleccionado.
        proyecto_id (int): ID del proyecto asociado al documento.
        frame_visual (tk.Frame): Frame donde se mostrarán los capítulos y requisitos extraídos.
    """
    

    try:
                
        # Limpiar cualquier contenido previo del frame de visualización.
        limpiar_visualizador(frame_visual)      

        # Intentar extraer el texto del PDF.
        texto_pdf = extraer_contenido_pdf(ruta_archivo, "almacen/temporal", proyecto_id)
                
        if not texto_pdf:
            # Mostrar mensaje de error si no se pudo extraer texto.
            messagebox.showerror(
                traducciones["M_Error"],
                traducciones["M_No_se_pudo_extraer_texto_del_PDF"]
            )
            return
        # Dividir el texto en capítulos utilizando una expresión regular.
        capitulos = re.split(patron_devuelto, texto_pdf)
        lista_req_cap = []  # Lista para almacenar los capítulos y requisitos extraídos.
        contenido = ""  # Contenido a mostrar en el área de texto.

        for capitulo in capitulos:
            capitulo = capitulo.strip()  # Eliminar espacios en blanco.
            if not capitulo:
                continue
                    
            patron_completo=convertir_patron_capitulo(patron_devuelto)
            # Buscar el número y título del capítulo con una expresión regular.
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
                
                #limpiar
                for widget in frame_visual.winfo_children():
                    widget.destroy()

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
                    command=lambda: verificacion_version(
                        traducciones,
                        titulo_documento,
                        lista_req_cap,
                        contenido,
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


####################################### mantener #########################
def verificacion_version (traducciones,
    titulo_documento,
    lista_req_cap,
    requisitos_editados,
    ruta_archivo,
    proyecto_id,
    frame_visual):

    
    version=obtener_version(titulo_documento,proyecto_id)
    
        
    if not version:
        version = 1    
        return guardar_requisitos_completos_y_asociaciones (version, traducciones, titulo_documento, lista_req_cap,
                                                                    requisitos_editados,
                                                                    ruta_archivo,
                                                                    proyecto_id,
                                                                    frame_visual,)
    else:
        respuesta = messagebox.askquestion(
        "Documento existente",
        "El documento ya existe. ¿Deseas crear una nueva versión?" )
        if respuesta == "yes":
            nueva_version = version + 1
            return guardar_requisitos_completos_y_asociaciones (nueva_version, traducciones, titulo_documento, lista_req_cap,
                                                                    requisitos_editados,
                                                                    ruta_archivo,
                                                                    proyecto_id,
                                                                    frame_visual,)    
        else:
                # Cancelar el proceso
                messagebox.showinfo("Cancelado", "El proceso de guardado ha sido cancelado.")
                return None


def guardar_requisitos_completos_y_asociaciones(
    version, traducciones,
    titulo_documento,
    lista_req_cap,
    requisitos_editados,
    ruta_archivo,
    proyecto_id,
    frame_visual,
):

    try:
      
        # 1. Insertar el documento en la base de datos.
        insertar_documento(titulo_documento, version, proyecto_id)
        documento_id = obtener_iddocumento(titulo_documento, proyecto_id, version)

        # 2. Procesar y guardar los requisitos.
        for capitulo, texto_requisito in lista_req_cap:
            insertar_requisito(capitulo, texto_requisito, documento_id)

        # 3. Renombrar y mover tablas e imágenes.
        mover_archivos_desde_temporal(documento_id,version)

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


def mover_archivos_desde_temporal(documento_id,version):
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
            nuevo_nombre = f"{nombre}D{documento_id:02}V{version:02}{ext}"
            archivo_origen = os.path.join(temporal_path, archivo)
            archivo_destino = os.path.join(permanente_path, nuevo_nombre)

            # Mover el archivo
            shutil.move(archivo_origen, archivo_destino)
            print(f"Archivo movido: {archivo_origen} -> {archivo_destino}")


