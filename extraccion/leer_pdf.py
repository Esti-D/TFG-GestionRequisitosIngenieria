import pdfplumber


def extraer_texto_pdf(ruta_pdf):
    """Función para extraer el texto de un archivo PDF."""
    texto_completo = ""
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                texto_completo += pagina.extract_text() + "\n"
    except Exception as e:
        print(f"Error al leer el archivo PDF: {e}")

    return texto_completo
