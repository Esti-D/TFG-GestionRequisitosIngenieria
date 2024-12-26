"""
Archivo: bloque_ayuda.py
Descripción: Este archivo contiene la función para abrir una ventana de ayuda que muestra
contenido en Markdown convertido a HTML, con soporte multilingüe.

Autor: Estíbalitz Díez
Fecha: 26/12/2024
Versión: 2
"""

import tkinter as tk
import os
from tkinterweb import HtmlFrame
import markdown2


def abrir_ayuda(traducciones, frame_visual):
    """
    Abre una ventana nueva para mostrar el contenido del archivo de ayuda en el idioma actual
     de la aplicación.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        frame_visual (tk.Frame): Frame principal de la interfaz donde se integra la funcionalidad.

    Funcionalidad:
        - Verifica que el archivo de ayuda correspondiente al idioma actual exista.
        - Convierte el archivo Markdown a HTML y lo muestra en una ventana emergente.
        - Personaliza la ventana con un título y un icono.
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
            f"{traducciones["M_El_archivo_de_ayuda"]} {idioma_actual}",
            f" {traducciones["M_no_existe_en"]} {ruta_ayuda}.",
        )
        return

    # Crear una nueva ventana de ayuda
    ventana_ayuda = tk.Toplevel()
    ventana_ayuda.title(traducciones["HELP_RM_Requirements_Management"])
    ventana_ayuda.geometry("800x600")

    # Incluir el logo en la barra del software
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.abspath(os.path.join(ruta_base, "..", "..", ".."))
    ruta_icono = os.path.join(
        ruta_raiz, "logos", "logo_reducido.ico"
    )  # Ruta del icono de la aplicación
    ventana_ayuda.iconbitmap(ruta_icono)  # Asignar icono a la ventana

    # Leer el archivo de ayuda en Markdown y convertirlo a HTML
    with open(ruta_ayuda, "r", encoding="utf-8") as archivo:
        contenido_md = archivo.read()
        contenido_html = markdown2.markdown(contenido_md)  # Convierte Markdown a HTML

    # Usa HtmlFrame para mostrar el contenido HTML
    html_frame = HtmlFrame(ventana_ayuda)
    html_frame.load_html(contenido_html)  # Inserta el contenido HTML en el frame
    html_frame.pack(expand=True, fill="both")
