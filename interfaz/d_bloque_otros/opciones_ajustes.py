import os
import subprocess
import sys
import tkinter as tk


def abrir_ajustes(traducciones, frame_visual):
    """Función para abrir la ventana o interfaz de ajustes."""
    # Limpiar el visualizador para mostrar la ventana de ajustes
    limpiar_visualizador(frame_visual)

    # Crear un título para la sección de ajustes
    label_ajustes = tk.Label(
        frame_visual, text=traducciones["M_Configuracion_Ajustes"], font=("Arial", 16)
    )
    label_ajustes.pack(pady=20)

    # Botón para cambiar el idioma
    boton_cambiar_idioma = tk.Button(
        frame_visual,
        text=traducciones["B_Cambiar_Idioma"],
        command=lambda: reiniciar_aplicacion(),
    )
    boton_cambiar_idioma.pack(pady=10)


# def reiniciar_aplicacion():
#   """Reinicia la aplicación ejecutando de nuevo `main.py`."""
#   python = sys.executable
#   os.execl(python, python, *sys.argv)


def reiniciar_aplicacion():
    """Reinicia la aplicación utilizando el mismo intérprete de Python."""
    try:
        nuevo_proceso = subprocess.Popen([sys.executable] + sys.argv)

        # Cierra el proceso actual para evitar que ambos queden abiertos
        os._exit(
            0
        )  # Es más seguro que sys.exit() en este caso para asegurar cierre inmediato

    except subprocess.CalledProcessError as e:
        print(f"Error al reiniciar la aplicación: {e}")


def limpiar_visualizador(frame_visual):
    """Función para limpiar el frame visual de la interfaz."""
    for widget in frame_visual.winfo_children():
        widget.destroy()
