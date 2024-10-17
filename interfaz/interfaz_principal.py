import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json #importar la libreria json

# Importar funciones específicas de otros módulos
from interfaz.a_bloque_load.interfaz_load import crear_bloque_load
from interfaz.b_bloque_consulta.interfaz_consulta import crear_bloque_consulta
from interfaz.c_bloque_acciones_independientes.interfaz_acciones import crear_bloque_acciones

from .bloque_ajustes import abrir_ajustes


# Cargar el archivo de idioma
def cargar_idioma():
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_idioma = os.path.join(ruta_base, 'd_bloque_ajustes', 'idioma_castellano.json')
    try:
        with open(ruta_idioma, 'r', encoding='utf-8') as archivo:
            traducciones = json.load(archivo)
            return traducciones
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {ruta_idioma}")
        return {}
    except json.JSONDecodeError:
        print("Error: El archivo no está en un formato JSON válido.")
        return {}
  

# Función para limpiar el visualizador
def limpiar_visualizador(frame_visual):
    """Elimina todos los widgets dentro del frame de visualización."""
    for widget in frame_visual.winfo_children():
        widget.destroy()


# FUNCION PRINCIPAL INTERFAZ  que encapsula toda la lógica de la interfaz
def interfaz_principal(db_path):

    # Cargar las traducciones del archivo JSON
    traducciones = cargar_idioma()
    
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("RM Requirements Management")
    ventana.state('zoomed')  # Maximizar la ventana

    # Incluir el logo en la barra del software
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.abspath(os.path.join(ruta_base,'..'))
    ruta_icono = os.path.join(ruta_raiz,'logos', "logo_reducido.ico")  # Ruta del icono de la aplicación
    ventana.iconbitmap(ruta_icono)  # Asignar icono a la ventana

    # Configurar la ventana para que el bloque gris esté dividido en dos partes (izquierda y derecha)
    ventana.grid_columnconfigure(0, weight=1)  # Parte izquierda para botones
    ventana.grid_columnconfigure(1, weight=7)  # Parte derecha para visualización
    ventana.grid_rowconfigure(0, weight=1)


    # Crear el frame para la visualización (parte derecha)
    frame_visual = tk.Frame(ventana, bg="white")
    frame_visual.grid(row=0, column=1, sticky="nsew")

    # Cargar imagen de fondo para la parte visual
    ruta_fondo = os.path.join(ruta_raiz, 'logos', "logofondo4.png")  # Ruta de la imagen de fondo
    imagen_fondo = Image.open(ruta_fondo)
    imagen_fondo = imagen_fondo.resize((800, 600))  # Ajustar el tamaño de la imagen
    imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)  # Convertir la imagen a formato compatible con Tkinter
    label_fondo = tk.Label(frame_visual, image=imagen_fondo_tk, bg="white")
    label_fondo.pack(expand=True)


    # Crear el frame para las funcionalidades (parte izquierda)
    frame_funcionalidades = tk.Frame(ventana, bg="#125ca6", padx=30, pady=20)  # #"lightgray" Ajustamos el padding para mayor expansión
    frame_funcionalidades.grid(row=0, column=0, sticky="nsew")
    
    #ventana.grid_columnconfigure(0, maxsize=300)  # Límite máximo de expansión
  
    # Configurar la expansión dentro del frame de funcionalidades
    frame_funcionalidades.grid_columnconfigure(0, weight=1)  # Aseguramos que la única columna ocupe todo el espacio

    # Color azul del logo 
    color_azul_logo = "#125ca6"

    ### BLOQUE 1: LOAD
    crear_bloque_load(frame_funcionalidades, traducciones, frame_visual)
    
    
    ### BLOQUE 2: CONSULTA
    crear_bloque_consulta(frame_funcionalidades, traducciones, frame_visual)
    

    ### BLOQUE 3: ACCIONES
    crear_bloque_acciones(frame_funcionalidades, traducciones, frame_visual)

   # Botón Ajustes (lo colocamos debajo de Eliminar)
    boton_ajustes = tk.Button(frame_funcionalidades, text=traducciones["P_AJUSTES"], command=lambda: abrir_ajustes(frame_visual))
    boton_ajustes.grid(row=3, column=0, padx=10, pady=8, sticky="ew", ipady=8)

    # Ejecutar el mainloop de la ventana
    ventana.mainloop()

