"""
Archivo: selector_idioma.py
Descripción: Funciones para la selección y carga de archivos de idioma en formato JSON para la interfaz gráfica.
Autor: Estíbalitz Díez
Fecha: 23/12/2024
Versión: 2
"""

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
    ruta_base = os.path.dirname(os.path.abspath(__file__))  # Ruta base del archivo
    ruta_idioma = os.path.join(ruta_base, archivo_idioma)  # Ruta completa del archivo de idioma

    try:
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
    # Crear la ventana para seleccionar el idioma
    ventana_idioma = tk.Tk()
    ventana_idioma.title("RM Requirements Management")
    ventana_idioma.geometry("300x150")

    # Configurar el icono de la ventana
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.abspath(os.path.join(ruta_base, ".."))
    ruta_icono = os.path.join(ruta_raiz, "logos", "logo_reducido.ico")
    ventana_idioma.iconbitmap(ruta_icono)

    # Opciones de idioma disponibles
    opciones_idioma = {
        "Castellano": "idioma_castellano.json",
        "Inglés": "idioma_ingles.json",
        "Francés": "idioma_frances.json",
    }

    # Variable para almacenar el idioma seleccionado
    idioma_seleccionado = tk.StringVar()

    # Crear un combobox para la selección de idioma
    combobox_idioma = ttk.Combobox(
        ventana_idioma, textvariable=idioma_seleccionado, state="readonly"
    )
    combobox_idioma["values"] = list(opciones_idioma.keys())  # Opciones del combobox
    combobox_idioma.set("Selecciona_Idioma")  # Texto inicial
    combobox_idioma.pack(pady=10)

    # Diccionario para almacenar las traducciones cargadas
    traducciones = {}

    # Función para confirmar la selección del idioma
    def confirmar_idioma():
        """
        Carga el archivo de idioma seleccionado y cierra la ventana.
        """
        idioma = idioma_seleccionado.get()  # Idioma seleccionado
        archivo_idioma = opciones_idioma.get(
            idioma, "idioma_castellano.json"
        )  # Archivo correspondiente
        traducciones.update(cargar_idioma(archivo_idioma))  # Cargar las traducciones
        ventana_idioma.quit()  # Terminar el loop de la ventana

    # Botón para confirmar la selección del idioma
    boton_confirmar = tk.Button(
        ventana_idioma, text="Confirmar", command=confirmar_idioma
    )
    boton_confirmar.pack(pady=10)

    # Iniciar el loop de la ventana
    ventana_idioma.mainloop()
    ventana_idioma.destroy()  # Destruir la ventana después de cerrarla

    return traducciones
