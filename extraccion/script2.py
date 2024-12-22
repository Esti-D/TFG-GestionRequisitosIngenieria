import os
import fitz  # PyMuPDF
import re


def analizar_documento(ruta_pdf):
    """
    Analiza las primeras páginas del PDF para detectar patrones de capítulos, encabezados y pies de página.

    Args:
        ruta_pdf (str): Ruta al archivo PDF.

    Returns:
        dict: Diccionario con patrones detectados (capítulos, encabezados, pies, etc.).
    """
    patrones = {
        "capitulos": None,
        "encabezados": None,
        "pies": None,
    }

    with fitz.open(ruta_pdf) as pdf_document:
        patrones_capitulos = set()
        encabezados = set()
        pies = set()

        # Analizar las primeras y últimas páginas
        for num_pagina, pagina in enumerate(pdf_document, start=1):
            texto = pagina.get_text("text")
            lineas = texto.splitlines()

            for linea in lineas:
                linea = linea.strip()
                if not linea:
                    continue

                # Detectar posibles capítulos
                if re.match(r"^\d+(\.|-)?\s+[A-Za-z]", linea):
                    patrones_capitulos.add(linea)

                # Identificar encabezados o pies (líneas repetidas)
                if num_pagina == 1 or num_pagina == len(pdf_document):
                    if linea.isupper() or len(linea.split()) <= 5:
                        if num_pagina == 1:
                            encabezados.add(linea)
                        else:
                            pies.add(linea)

        patrones["capitulos"] = patrones_capitulos
        patrones["encabezados"] = encabezados
        patrones["pies"] = pies

    return patrones


def extraer_contenido_pdf_analizado(ruta_pdf, patrones):
    """
    Extrae contenido del PDF aplicando patrones identificados previamente.

    Args:
        ruta_pdf (str): Ruta al archivo PDF.
        patrones (dict): Patrones identificados para capítulos, encabezados y pies.

    Returns:
        str: Contenido procesado del PDF.
    """
    contenido_completo = ""

    with fitz.open(ruta_pdf) as pdf_document:
        for num_pagina, pagina in enumerate(pdf_document, start=1):
            texto_pagina = pagina.get_text("text")
            lineas = texto_pagina.splitlines()

            for linea in lineas:
                linea = linea.strip()
                if not linea:
                    continue

                # Ignorar encabezados y pies de página
                if linea in patrones["encabezados"] or linea in patrones["pies"]:
                    continue

                # Procesar capítulos y contenido
                if any(re.match(patron, linea) for patron in patrones["capitulos"]):
                    contenido_completo += f"CAPÍTULO: {linea}\n"
                else:
                    contenido_completo += linea + "\n"

    return contenido_completo
