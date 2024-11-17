import pdfplumber


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
