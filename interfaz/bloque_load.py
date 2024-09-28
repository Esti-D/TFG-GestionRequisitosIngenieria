import tkinter as tk

# Función para crear el bloque de carga de archivos
def crear_boton_load(frame_funcionalidades):
    # Botón para cargar el archivo (LOAD)
    boton_load = tk.Button(frame_funcionalidades, text="LOAD")
    boton_load.grid(row=0, column=0, padx=10, pady=10, sticky="ew", ipady=10)

    # Botón para abrir explorador de archivos
    boton_seleccionar = tk.Button(frame_funcionalidades, text="Seleccionar archivo")
    boton_seleccionar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Cuadro de texto para mostrar la ruta seleccionada (debajo de seleccionar archivo)
    entry_archivo = tk.Entry(frame_funcionalidades)
    entry_archivo.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
