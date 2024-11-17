import tkinter as tk
from tkinter import ttk
import os
import json


def cargar_idioma(archivo_idioma="idioma_castellano.json"):
    """
    Carga un archivo de idioma en formato JSON y devuelve un diccionario con las traducciones.

    Args:
        archivo_idioma (str): Nombre del archivo JSON que contiene las traducciones.
                              Por defecto, se utiliza "idioma_castellano.json".

    Returns:
        dict: Diccionario con las traducciones cargadas.
              Si hay un error, devuelve un diccionario vacío.
    """
    # Obtener la ruta completa del archivo de idioma
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_idioma = os.path.join(ruta_base, archivo_idioma)

    try:
        # Abrir y cargar el archivo JSON con codificación UTF-8
        with open(ruta_idioma, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {ruta_idioma}")
        return {}
    except json.JSONDecodeError:
        print("Error: El archivo no está en un formato JSON válido.")
        return {}


def seleccionar_idioma():
    """
    Muestra una ventana para seleccionar el idioma y carga las traducciones correspondientes.

    Returns:
        dict: Diccionario con las traducciones del idioma seleccionado.
    """
    # Crear ventana para seleccionar idioma
    ventana_idioma = tk.Tk()
    ventana_idioma.title("RM Requirements Management")
    ventana_idioma.geometry("300x150")

    # Configurar el icono de la ventana
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.abspath(os.path.join(ruta_base, ".."))
    ruta_icono = os.path.join(ruta_raiz, "logos", "logo_reducido.ico")
    ventana_idioma.iconbitmap(ruta_icono)

    # Opciones de idiomas disponibles
    opciones_idioma = {
        "Castellano": "idioma_castellano.json",
        "Inglés": "idioma_ingles.json",
        "Francés": "idioma_frances.json",
    }

    # Variable para almacenar el idioma seleccionado
    idioma_seleccionado = tk.StringVar()

    # Crear un combobox con las opciones de idioma
    combobox_idioma = ttk.Combobox(
        ventana_idioma, textvariable=idioma_seleccionado, state="readonly"
    )
    combobox_idioma["values"] = list(opciones_idioma.keys())  # Rellenar con idiomas
    combobox_idioma.set("Selecciona_Idioma")  # Texto inicial del combobox
    combobox_idioma.pack(pady=10)

    # Diccionario para almacenar las traducciones cargadas
    traducciones = {}

    # Función para confirmar la selección de idioma
    def confirmar_idioma():
        """
        Carga el archivo de idioma seleccionado y cierra la ventana.
        """
        idioma = idioma_seleccionado.get()  # Obtener el idioma seleccionado
        archivo_idioma = opciones_idioma.get(
            idioma, "idioma_castellano.json"
        )  # Archivo correspondiente
        traducciones.update(cargar_idioma(archivo_idioma))  # Cargar traducciones
        ventana_idioma.quit()  # Finalizar el loop de la ventana

    # Botón para confirmar la selección
    boton_confirmar = tk.Button(
        ventana_idioma, text="Confirmar", command=confirmar_idioma
    )
    boton_confirmar.pack(pady=10)

    # Iniciar el loop de la ventana
    ventana_idioma.mainloop()
    ventana_idioma.destroy()  # Destruir la ventana después de cerrarla

    return traducciones
