import logging
import pdfplumber
import fitz
import os
import csv

def extraer_texto_pdf(ruta_pdf):
    """
    Extrae todo el texto de un archivo PDF.

    Args:
        ruta_pdf (str): Ruta al archivo PDF del cual se desea extraer el texto.

    Returns:
        str: Texto completo extraído del archivo PDF. Si ocurre algún error, devuelve una cadena vacía.
    """
    texto_completo = ""  # Variable para almacenar el texto extraído

    try:
        # Abrir el archivo PDF usando pdfplumber
        with pdfplumber.open(ruta_pdf) as pdf:
            # Iterar por cada página del PDF
            for pagina in pdf.pages:
                # Extraer el texto de la página actual y añadirlo a la variable
                texto_completo += pagina.extract_text() + "\n"
    except Exception as e:
        # Manejar errores durante la lectura del PDF y mostrar un mensaje
        print(f"Error al leer el archivo PDF: {e}")

    return (
        texto_completo  # Devolver el texto extraído o una cadena vacía en caso de error
    )

def extraer_contenido_pdf_anterior(ruta_pdf, ruta_temporal, proyecto_id, titulo_documento):
    """
    Extrae contenido de un PDF (texto, tablas e imágenes) en el orden en que aparece en el documento.

    Args:
        ruta_pdf (str): Ruta al archivo PDF del cual se desea extraer el contenido.
        ruta_temporal (str): Ruta a la carpeta temporal donde se almacenarán imágenes y tablas.
        proyecto_id (int): ID del proyecto asociado al documento.
        titulo_documento (str): Nombre del documento.

    Returns:
        str: Contenido completo del PDF con texto y codificaciones de tablas e imágenes.
    """
    contenido_completo = ""  # Variable para almacenar el contenido completo extraído
    contador_tablas = 1
    contador_imagenes = 1

    # Asegurar que la carpeta temporal exista y esté vacía
    if not os.path.exists(ruta_temporal):
        os.makedirs(ruta_temporal)
    else:
        for archivo in os.listdir(ruta_temporal):
            os.remove(os.path.join(ruta_temporal, archivo))

    try:
        # Abrir el documento con pdfplumber para texto y tablas
        with pdfplumber.open(ruta_pdf) as pdf:
            pdf_document = fitz.open(ruta_pdf)  # Abrir el documento con PyMuPDF para imágenes

            for i, pagina in enumerate(pdf.pages, start=1):
                texto_pagina = pagina.extract_text() or ""

                # Agregar el texto al contenido
                if texto_pagina.strip():
                    contenido_completo += texto_pagina + "\n"

                # Detectar tablas
                tablas = pagina.extract_tables()
                for tabla in tablas:
                    codigo_tabla = f"EGP_TAB_P{proyecto_id:03}_D{titulo_documento:03}_{contador_tablas}"
                    archivo_csv = os.path.join(ruta_temporal, f"{codigo_tabla}.csv")
                    guardar_tabla_csv(tabla, archivo_csv)
                    contenido_completo += f"{codigo_tabla}\n"
                    contador_tablas += 1

                # Detectar imágenes para esta página con PyMuPDF
                page_mupdf = pdf_document[i - 1]  # PyMuPDF utiliza índices 0-based
                images = page_mupdf.get_images(full=True)
                for img_index, img in enumerate(images, start=1):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    ext = base_image["ext"]
                    codigo_imagen = f"EGP_FIG_P{proyecto_id:03}_D{titulo_documento:03}_{contador_imagenes}"
                    archivo_imagen = os.path.join(ruta_temporal, f"{codigo_imagen}.{ext}")

                    with open(archivo_imagen, "wb") as f:
                        f.write(image_bytes)

                    contenido_completo += f"{codigo_imagen}\n"
                    contador_imagenes += 1

    except Exception as e:
        print(f"Error al procesar el archivo PDF: {e}")

    return contenido_completo


def extraer_contenido_pdf(ruta_pdf, ruta_temporal, proyecto_id):
    """
    Extrae texto de un PDF y guarda imágenes/tablas en la carpeta temporal.

    Args:
        ruta_pdf (str): Ruta al archivo PDF.
        ruta_temporal (str): Carpeta temporal para guardar imágenes y tablas.
        proyecto_id (int): ID del proyecto asociado.

    Returns:
        str: Contenido completo del PDF (solo texto).
    """
    contenido_completo = ""
    contador_imagenes = 1
    contador_tablas = 1

    # Asegurar que la carpeta temporal exista y esté vacía
    if not os.path.exists(ruta_temporal):
        os.makedirs(ruta_temporal)
    else:
        for archivo in os.listdir(ruta_temporal):
            os.remove(os.path.join(ruta_temporal, archivo))

    try:
        # Abrir el PDF para procesar texto e imágenes
        pdf_document = fitz.open(ruta_pdf)
        with pdfplumber.open(ruta_pdf) as pdf:
            for num_pagina, pagina in enumerate(pdf.pages, start=1):
                # Extraer texto
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    contenido_completo += texto_pagina + "\n"

                # Extraer tablas y guardarlas en temporal
                tablas = pagina.extract_tables()
                for tabla in tablas:
                    codigo_tabla = f"TAB{contador_tablas:02}P{proyecto_id:02}"
                    archivo_csv = os.path.join(ruta_temporal, f"{codigo_tabla}.csv")
                    guardar_tabla_csv(tabla, archivo_csv)
                    contador_tablas += 1

                # Extraer imágenes y guardarlas en temporal
                page_mupdf = pdf_document[num_pagina - 1]  # PyMuPDF usa índice 0-based
                for img_index, img in enumerate(page_mupdf.get_images(full=True), start=1):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    if not base_image or "image" not in base_image:
                        continue

                    image_bytes = base_image["image"]
                    ext = base_image["ext"]
                    codigo_imagen = f"FIG{contador_imagenes:02}P{proyecto_id:02}"
                    archivo_imagen = os.path.join(ruta_temporal, f"{codigo_imagen}.{ext}")

                    with open(archivo_imagen, "wb") as f:
                        f.write(image_bytes)

                    contador_imagenes += 1

    except Exception as e:
        print(f"Error al procesar el archivo PDF: {e}")

    print(contenido_completo)
    return contenido_completo



def guardar_tabla_csv(tabla, archivo_csv):
    """
    Guarda una tabla detectada en un archivo CSV.

    Args:
        tabla (list): Lista de filas representando la tabla.
        archivo_csv (str): Ruta al archivo CSV donde se guardará la tabla.
    """
    import csv

    with open(archivo_csv, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerows(tabla)