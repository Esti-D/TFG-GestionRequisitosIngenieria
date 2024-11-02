import tkinter as tk
import os
from tkinterweb import HtmlFrame
import markdown2



def abrir_ayuda(traducciones, frame_visual):
    """
    Abre una ventana nueva para mostrar el contenido del archivo de ayuda en el idioma actual de la aplicación.
    
    Args:
    - frame_visual: el frame principal de la interfaz.
    - idioma_actual: el idioma en el que está configurada la aplicación (ej. "castellano", "ingles", "frances").
    """
    idioma_actual= traducciones["IDIOMA"]
    #idioma_actual= "castellano"
    # Rutas a los archivos de ayuda en distintos idiomas
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    archivos_ayuda = {
        "castellano": os.path.join(ruta_base, "help_castellano.md"),
        "ingles": os.path.join(ruta_base, "help_ingles.md"),
        "frances": os.path.join(ruta_base, "help_frances.md")
    }

    # Verificar que el archivo de ayuda en el idioma actual existe
    ruta_ayuda = archivos_ayuda.get(idioma_actual)
    if not ruta_ayuda or not os.path.exists(ruta_ayuda):
        print(f"{traducciones["M_El_archivo_de_ayuda"]} {idioma_actual} {traducciones["M_no_existe_en "]} {ruta_ayuda}.")
        return

    # Crear una nueva ventana de ayuda
    ventana_ayuda = tk.Toplevel()
    ventana_ayuda.title(traducciones["HELP_RM_Requirements_Management"])
    ventana_ayuda.geometry("800x600")

    # Leer el archivo de ayuda en Markdown y convertirlo a HTML
    with open(ruta_ayuda, "r", encoding="utf-8") as archivo:
        contenido_md = archivo.read()
        contenido_html = markdown2.markdown(contenido_md)  # Convierte Markdown a HTML

    # Usa HtmlFrame para mostrar el contenido HTML
    html_frame = HtmlFrame(ventana_ayuda)
    html_frame.load_html(contenido_html)  # Inserta el contenido HTML en el frame
    html_frame.pack(expand=True, fill="both")
    
    
