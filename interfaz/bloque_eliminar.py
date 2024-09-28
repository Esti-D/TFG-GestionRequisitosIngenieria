import tkinter as tk

# Función para limpiar el contenido del visualizador
def limpiar_visualizador(frame_visual):
    for widget in frame_visual.winfo_children():
        widget.destroy()

# Función para mostrar el formulario de Eliminar en el visualizador
def mostrar_formulario_eliminar(frame_visual):
    limpiar_visualizador(frame_visual)

    # Título del formulario
    label_titulo = tk.Label(frame_visual, text="Eliminar Elemento", font=("Arial", 16))
    label_titulo.pack(pady=20)

    # Entrada para el tipo de elemento (requisito, documento, proyecto, subsistema)
    label_tipo = tk.Label(frame_visual, text="Tipo de Elemento:")
    label_tipo.pack(pady=5)
    entry_tipo = tk.Entry(frame_visual)
    entry_tipo.pack(pady=5)

    # Entrada para el ID o código del elemento
    label_id = tk.Label(frame_visual, text="ID o Código:")
    label_id.pack(pady=5)
    entry_id = tk.Entry(frame_visual)
    entry_id.pack(pady=5)

    # Botón para eliminar
    boton_eliminar = tk.Button(frame_visual, text="Eliminar")
    boton_eliminar.pack(pady=20)

# Función para crear el botón de Eliminar
def crear_boton_eliminar(frame_funcionalidades, frame_visual):
    boton_eliminar = tk.Button(frame_funcionalidades, text="Eliminar", command=lambda: mostrar_formulario_eliminar(frame_visual))
    boton_eliminar.grid(row=8, column=0, padx=10, pady=10, sticky="ew", ipady=10)
