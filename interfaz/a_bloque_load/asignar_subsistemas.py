import tkinter as tk
from almacenamiento.func_relaciones import insertar_relacion_documento_subsistema
from almacenamiento.func_subsistemas import obtener_id_subsistema
from asignacion.asignacion_subsistemas import asignar_subsistemas_a_documento


def asignar_subsistemas_a_documento_y_mostrar_ventana(
    traducciones, texto_documento, documento_id, frame_visual
):
    """
    Crea una ventana emergente para mostrar los subsistemas sugeridos y permite asignarlos al documento.

    Args:
        traducciones (dict): Diccionario con las traducciones de los textos para la interfaz.
        texto_documento (str): Texto del documento a analizar para sugerir subsistemas.
        documento_id (int): ID del documento al que se asociarán los subsistemas seleccionados.
        frame_visual (tk.Frame): Frame de la interfaz para actualizar la vista si es necesario.

    Función principal:
        - Analiza el texto del documento y genera una lista de subsistemas sugeridos.
        - Crea una ventana emergente donde el usuario puede seleccionar los subsistemas aplicables.
        - Proporciona un botón para guardar las asociaciones seleccionadas en la base de datos.
    """
    # Obtener los subsistemas sugeridos basándose en el texto del documento.
    subsistemas_sugeridos = asignar_subsistemas_a_documento(texto_documento)

    # Crear una ventana emergente para la selección de subsistemas.
    ventana_subsistemas = tk.Toplevel()  # Crear ventana secundaria.
    ventana_subsistemas.title(traducciones["M_Asignacion_de_Subsistemas"])
    ventana_subsistemas.geometry("400x300")  # Configurar el tamaño de la ventana.

    # Etiqueta descriptiva en la ventana.
    tk.Label(
        ventana_subsistemas,
        text=traducciones["M_Subsistemas_sugeridos_para_el_documento"],
    ).pack(pady=10)

    # Lista para mostrar los subsistemas sugeridos.
    lista_subsistemas = tk.Listbox(
        ventana_subsistemas, selectmode=tk.MULTIPLE, height=10
    )
    for subsistema in subsistemas_sugeridos:
        lista_subsistemas.insert(tk.END, subsistema)  # Agregar subsistemas a la lista.
    lista_subsistemas.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Botón para aceptar y guardar la selección de subsistemas.
    boton_aceptar = tk.Button(
        ventana_subsistemas,
        text=traducciones["B_ACEPTAR"],
        command=lambda: aceptar_asignacion_subsistemas(
            documento_id, lista_subsistemas, ventana_subsistemas
        ),
    )
    boton_aceptar.pack(pady=10)


def aceptar_asignacion_subsistemas(
    documento_id, lista_subsistemas, ventana_subsistemas
):
    """
    Guarda los subsistemas seleccionados para el documento en la base de datos.

    Args:
        documento_id (int): ID del documento al que se asociarán los subsistemas.
        lista_subsistemas (tk.Listbox): Lista que contiene los subsistemas seleccionados por el usuario.
        ventana_subsistemas (tk.Toplevel): Ventana emergente que se cerrará después de guardar las asociaciones.

    Flujo:
        1. Obtiene los índices de los subsistemas seleccionados.
        2. Inserta cada subsistema como una relación con el documento en la base de datos.
        3. Cierra la ventana emergente tras guardar las asociaciones.
    """
    # Obtener los índices de los subsistemas seleccionados en la lista.
    seleccionados = lista_subsistemas.curselection()

    # Crear una lista con los nombres de los subsistemas seleccionados.
    subsistemas_asignados = [lista_subsistemas.get(i) for i in seleccionados]

    # Iterar sobre cada subsistema seleccionado para guardarlo en la base de datos.
    for subsistema in subsistemas_asignados:
        # Obtener el ID del subsistema desde la base de datos.
        subsistema_id = obtener_id_subsistema(subsistema)

        # Insertar la relación documento-subsistema en la base de datos.
        insertar_relacion_documento_subsistema(documento_id, subsistema_id)

        # Mensaje de depuración en la consola.
        print(
            f"Subsistemas asignados al documento {documento_id}: {subsistema}: {subsistema_id}"
        )

    # Cerrar la ventana emergente tras completar las asignaciones.
    ventana_subsistemas.destroy()
