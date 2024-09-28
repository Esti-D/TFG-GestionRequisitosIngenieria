import tkinter as tk

# Función para limpiar el contenido del visualizador
def limpiar_visualizador(frame_visual):
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Función para mostrar el formulario de Asignar en el visualizador
def mostrar_formulario_asignar(frame_visual):
    limpiar_visualizador(frame_visual)

    # Título del formulario
    label_titulo = tk.Label(frame_visual, text="Asignar Requisito", font=("Arial", 16))
    label_titulo.pack(pady=20)

    # Entrada para el código de documento
    label_documento = tk.Label(frame_visual, text="Código de Documento:")
    label_documento.pack(pady=5)
    entry_documento = tk.Entry(frame_visual)
    entry_documento.pack(pady=5)

    # Entrada para el subsistema
    label_subsistema = tk.Label(frame_visual, text="Subsistema:")
    label_subsistema.pack(pady=5)
    entry_subsistema = tk.Entry(frame_visual)
    entry_subsistema.pack(pady=5)

    # Botón para asignar
    boton_asignar = tk.Button(frame_visual, text="Asignar")
    boton_asignar.pack(pady=20)

# Función para crear el botón de Asignar
def crear_boton_asignar(frame_funcionalidades, frame_visual):
    boton_asignar = tk.Button(frame_funcionalidades, text="Asignar", command=lambda: mostrar_formulario_asignar(frame_visual))
    boton_asignar.grid(row=7, column=0, padx=10, pady=10, sticky="ew", ipady=10)
