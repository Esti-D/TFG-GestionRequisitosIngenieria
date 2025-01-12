"""
Archivo: bloque_ayuda.py - webview
Descripción: Este archivo contiene la función para abrir una ventana de ayuda que muestra
contenido en Markdown convertido a HTML, con soporte multilingüe.
"""

import os
import markdown2
import webview


def abrir_ayuda(traducciones, frame_visual):
    """
    Abre una ventana nueva para mostrar el contenido del archivo de ayuda en el idioma actual
    en un WebView.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        frame_visual (tk.Frame): Frame principal de la interfaz donde se integra la funcionalidad.
    """
    # Obtener el idioma actual desde las traducciones.
    idioma_actual = traducciones["IDIOMA"]

    # Rutas a los archivos de ayuda en distintos idiomas
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    archivos_ayuda = {
        "castellano": os.path.join(ruta_base, "help_castellano.md"),
        "ingles": os.path.join(ruta_base, "help_ingles.md"),
        "frances": os.path.join(ruta_base, "help_frances.md"),
    }

    # Verificar que el archivo de ayuda en el idioma actual existe
    ruta_ayuda = archivos_ayuda.get(idioma_actual)
    if not ruta_ayuda or not os.path.exists(ruta_ayuda):
        print(
            f"{traducciones['M_El_archivo_de_ayuda']} {idioma_actual}",
            f" {traducciones['M_no_existe_en']} {ruta_ayuda}.",
        )
        return

    # Leer el archivo de ayuda en Markdown y convertirlo a HTML
    with open(ruta_ayuda, "r", encoding="utf-8") as archivo:
        contenido_md = archivo.read()
        contenido_html = markdown2.markdown(contenido_md)  # Convierte Markdown a HTML

    # Mostrar el contenido HTML en un WebView
    webview.create_window(traducciones["HELP_RM_Requirements_Management"], html=contenido_html)
    webview.start()
