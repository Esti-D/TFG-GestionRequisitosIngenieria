import tkinter as tk
from tkinter import ttk
import os
import json

def cargar_idioma(archivo_idioma='idioma_castellano.json'):
    """Carga el archivo de idioma seleccionado y retorna las traducciones."""
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_idioma = os.path.join(ruta_base, archivo_idioma)
    try:
        with open(ruta_idioma, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {ruta_idioma}")
        return {}
    except json.JSONDecodeError:
        print("Error: El archivo no está en un formato JSON válido.")
        return {}

def seleccionar_idioma():
    """Abre una ventana para seleccionar el idioma y retorna las traducciones correspondientes."""
    ventana_idioma = tk.Tk()
    ventana_idioma.title=("SELECCION_IDIOMA")
    ventana_idioma.geometry("300x150")

    opciones_idioma = {
        "Castellano": "idioma_castellano.json",
        "Inglés": "idioma_ingles.json",
        "Francés": "idioma_frances.json"
    }

    idioma_seleccionado = tk.StringVar()
    combobox_idioma = ttk.Combobox(ventana_idioma, textvariable=idioma_seleccionado, state="readonly")
    combobox_idioma['values'] = list(opciones_idioma.keys())
    combobox_idioma.set("Selecciona_Idioma")
    combobox_idioma.pack(pady=10)

    traducciones = {}

    def confirmar_idioma():
        idioma = idioma_seleccionado.get()
        archivo_idioma = opciones_idioma.get(idioma, "idioma_castellano.json")
        traducciones.update(cargar_idioma(archivo_idioma))
        ventana_idioma.quit()

    boton_confirmar = tk.Button(ventana_idioma, text="Confirmar", command=confirmar_idioma)
    boton_confirmar.pack(pady=10)

    ventana_idioma.mainloop()
    ventana_idioma.destroy()
    
    return traducciones
