import os
import fitz  # PyMuPDF
import re

def buscar_capitulos(contenido):
    """
    Detecta capítulos en el contenido del PDF.

    Args:
        contenido (str): Texto completo del PDF.

    Returns:
        list: Lista de capítulos detectados.
    """
    lineas = contenido.splitlines()
    capitulos = []

    # Patrón para detectar capítulos
    patron_capitulo = re.compile(r"^\d+(\.\d+)*(\.|-|\\)?\s+[A-Za-z0-9]")

    for linea in lineas:
        if patron_capitulo.match(linea):
            capitulos.append(linea.strip())

    return capitulos


def analizar_documento_con_posicion(ruta_pdf):
    """
    Analiza el PDF para detectar encabezados y pies basados en su posición y repetición.

    Args:
        ruta_pdf (str): Ruta al archivo PDF.

    Returns:
        dict: Diccionario con encabezados y pies detectados.
    """
    encabezados = set()
    pies = set()

    try:
        with fitz.open(ruta_pdf) as pdf_document:
            for num_pagina, pagina in enumerate(pdf_document, start=1):
                altura_pagina = pagina.rect.height
                bloques = pagina.get_text("blocks")  # Obtener bloques de texto con coordenadas

                for bloque in bloques:
                    x0, y0, x1, y1, contenido = bloque[:5]  # Coordenadas y texto del bloque
                    contenido = contenido.strip()

                    # Detectar encabezados (bloques cerca del borde superior)
                    if y0 < 57:
                        encabezados.add(contenido)

                    # Detectar pies (bloques cerca del borde inferior)
                    if y1 > altura_pagina - 57:
                        pies.add(contenido)

    except Exception as e:
        print(f"Error al analizar el documento: {e}")

    return {"encabezados": encabezados, "pies": pies}


def filtrar_contenido(contenido, encabezados, pies):
    """
    Elimina líneas que coincidan con encabezados o pies detectados.

    Args:
        contenido (str): Texto completo del PDF.
        encabezados (set): Conjunto de encabezados detectados.
        pies (set): Conjunto de pies detectados.

    Returns:
        str: Contenido limpio de encabezados y pies.
    """
    lineas = contenido.splitlines()
    contenido_filtrado = []

    for linea in lineas:
        if linea.strip() in encabezados or linea.strip() in pies:
            continue  # Ignorar encabezados y pies
        contenido_filtrado.append(linea)

    return "\n".join(contenido_filtrado)


def extraer_contenido_pdf_nuevo(ruta_pdf):
    """
    Extrae texto limpio de un PDF (sin encabezados ni pies).

    Args:
        ruta_pdf (str): Ruta al archivo PDF.

    Returns:
        str: Contenido limpio del PDF.
    """
    contenido_original = ""
    contenido_limpio = ""

    try:
        # Paso 1: Obtener contenido original
        with fitz.open(ruta_pdf) as pdf_document:
            for pagina in pdf_document:
                contenido_original += pagina.get_text("text") + "\n"

        # Paso 2: Detectar encabezados y pies
        patrones = analizar_documento_con_posicion(ruta_pdf)
        encabezados = patrones["encabezados"]
        pies = patrones["pies"]

        # Paso 3: Filtrar encabezados y pies
        contenido_limpio = filtrar_contenido(contenido_original, encabezados, pies)

    except Exception as e:
        print(f"Error al procesar el archivo PDF: {e}")

    return contenido_limpio


ruta_pdf = "PDFDEMO20.pdf"
contenido = extraer_contenido_pdf_nuevo(ruta_pdf)
print("Texto limpio extraído:\n", contenido)