import tkinter as tk
from PIL import Image, ImageTk
import os
import sys


# Importar funciones específicas de otros módulos
from interfaz.a_bloque_load.interfaz_load import crear_bloque_load
from interfaz.b_bloque_consulta.interfaz_consulta import crear_bloque_consulta
from interfaz.c_bloque_acciones_independientes.interfaz_acciones import (
    crear_bloque_acciones,
)
from interfaz.d_bloque_otros.interfaz_otros import crear_bloque_otros


def limpiar_visualizador(frame_visual):
    """
    Elimina todos los widgets dentro del frame de visualización.

    Args:
        frame_visual (tk.Frame): Frame donde se visualizan los contenidos dinámicos.
    """
    for widget in frame_visual.winfo_children():
        widget.destroy()


# FUNCION PRINCIPAL INTERFAZ  que encapsula toda la lógica de la interfaz
def interfaz_principal(traducciones, db_path):
    """
    Configura e inicia la interfaz gráfica de usuario principal de la aplicación.

    La interfaz está dividida en dos secciones principales:
    1. **Panel de funcionalidades (izquierda):** Contiene botones y bloques funcionales.
    2. **Área de visualización (derecha):** Muestra contenido dinámico basado en las acciones del usuario.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        db_path (str): Ruta a la base de datos utilizada por la aplicación.

    Estructura:
    - Carga de un fondo gráfico.
    - Inclusión de un icono para la ventana.
    - División en bloques funcionales: `LOAD`, `CONSULTA`, `ACCIONES`, y `OTROS`.

    Raises:
        FileNotFoundError: Si los archivos de icono o fondo no se encuentran en las rutas especificadas.
    """

    # Crear ventana principal
    ventana = tk.Tk()
    ventana.withdraw()  # Oculta la ventana durante la configuración inicial

    ventana.title("RM Requirements Management")
    ventana.state("zoomed")  # Maximizar la ventana

    # Incluir el logo en la barra del software
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.abspath(os.path.join(ruta_base, ".."))
    ruta_icono = os.path.join(
        ruta_raiz, "logos", "logo_reducido.ico"
    )  # Ruta del icono de la aplicación
    ventana.iconbitmap(ruta_icono)  # Asignar icono a la ventana

    def on_closing():
        """
        Maneja el cierre de la ventana principal para garantizar que el proceso termine completamente.
        """
        print("Cerrando la aplicación ...")
        os._exit(0)  # Fuerza la salida inmediata del proceso

    ventana.protocol("WM_DELETE_WINDOW", on_closing)

    # Configurar la ventana para que el bloque gris esté dividido en dos partes (izquierda y derecha)
    ventana.grid_columnconfigure(0, weight=1)  # Parte izquierda para botones
    ventana.grid_columnconfigure(1, weight=7)  # Parte derecha para visualización
    ventana.grid_rowconfigure(0, weight=1)

    # Crear el frame para la visualización (parte derecha)
    frame_visual = tk.Frame(ventana, bg="white")
    frame_visual.grid(row=0, column=1, sticky="nsew")

    # Cargar imagen de fondo para la parte visual
    ruta_fondo = os.path.join(
        ruta_raiz, "logos", "logofondo4.png"
    )  # Ruta de la imagen de fondo
    imagen_fondo = Image.open(ruta_fondo)
    imagen_fondo = imagen_fondo.resize((700, 500))  # Ajustar el tamaño de la imagen
    imagen_fondo_tk = ImageTk.PhotoImage(
        imagen_fondo
    )  # Convertir la imagen a formato compatible con Tkinter
    label_fondo = tk.Label(frame_visual, image=imagen_fondo_tk, bg="white")
    label_fondo.pack(expand=True)

    # Crear el frame para las funcionalidades (parte izquierda)
    frame_funcionalidades = tk.Frame(
        ventana, bg="#125ca6", padx=30, pady=20
    )  # #"lightgray" Ajustamos el padding para mayor expansión
    frame_funcionalidades.grid(row=0, column=0, sticky="nsew")

    # Configurar la expansión dentro del frame de funcionalidades
    frame_funcionalidades.grid_columnconfigure(
        0, weight=1
    )  # Aseguramos que la única columna ocupe todo el espacio

    # Color azul del logo
    color_azul_logo = "#125ca6"

    ### BLOQUE 1: LOAD
    crear_bloque_load(frame_funcionalidades, traducciones, frame_visual)

    ### BLOQUE 2: CONSULTA
    crear_bloque_consulta(frame_funcionalidades, traducciones, frame_visual)

    ### BLOQUE 3: ACCIONES
    crear_bloque_acciones(frame_funcionalidades, traducciones, frame_visual)

    ### BLOQUE 4: OTROS
    crear_bloque_otros(frame_funcionalidades, traducciones, frame_visual)

    ventana.deiconify()  # Muestra la ventana ya maximizada

    # Ejecutar el mainloop de la ventana
    ventana.mainloop()
