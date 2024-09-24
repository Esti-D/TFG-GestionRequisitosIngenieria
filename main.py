from extraccion.leer_pdf import extraer_texto_pdf

if __name__ == "__main__":
    ruta_pdf = "PDF/PDF1.pdf"
    print(f"Intentando abrir el archivo: {ruta_pdf}")  # Mensaje de depuración
    texto = extraer_texto_pdf(ruta_pdf)
    print(texto)
