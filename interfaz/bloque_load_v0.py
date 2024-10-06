import tkinter as tk
from tkinter import messagebox, filedialog  # Para abrir el explorador de archivos y mostrar mensajes
from extraccion.leer_pdf import extraer_texto_pdf
from almacenamiento.func_documentos import insertar_documento
from almacenamiento.func_requisitos import insertar_requisito
from almacenamiento.func_ciudades import obtener_ciudades
from interfaz.bloque_asignar import limpiar_visualizador  # Para limpiar la ventana visual
from asignacion.asignacion_subsistemas import asignar_subsistemas_a_documento  # Lógica para asignar subsistemas

# Función para crear el bloque de carga de archivos (botones y cuadro de entrada)
def crear_boton_load(frame_funcionalidades):
    """Crea los botones de LOAD y Seleccionar archivo, así como el cuadro de entrada para la ruta."""
    boton_load = tk.Button(frame_funcionalidades, text="LOAD")
    boton_load.grid(row=0, column=0, padx=10, pady=10, sticky="ew", ipady=10)

    boton_seleccionar = tk.Button(frame_funcionalidades, text="Seleccionar archivo")
    boton_seleccionar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    entry_archivo = tk.Entry(frame_funcionalidades)  # Cuadro de texto para mostrar la ruta seleccionada
    entry_archivo.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Función para abrir el explorador y seleccionar un archivo PDF
def seleccionar_archivo(entry_archivo):
    """Abre el explorador de archivos para seleccionar un archivo PDF y muestra la ruta en el cuadro de texto."""
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]  # Filtrar solo archivos PDF
    )
    if archivo:
        entry_archivo.delete(0, tk.END)  # Limpiar el cuadro de texto
        entry_archivo.insert(0, archivo)  # Mostrar la ruta del archivo seleccionado

# Función para seleccionar una ciudad/proyecto para asociar al documento
def ventana_seleccionar_proyecto(callback):
    """Crea una ventana para seleccionar un proyecto de una lista y luego llama al callback con el proyecto seleccionado."""
    ventana = tk.Toplevel()
    ventana.title("Seleccionar Proyecto")
    ventana.geometry("400x300")  # Ajustar tamaño de la ventana

    proyectos = obtener_ciudades()  # Obtener lista de proyectos desde la base de datos

    # Listbox para mostrar proyectos
    lista_proyectos = tk.Listbox(ventana, height=10)
    for proyecto in proyectos:
        lista_proyectos.insert(tk.END, proyecto[1])  # Insertar solo el nombre del proyecto
    lista_proyectos.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Botón para aceptar la selección
    boton_aceptar = tk.Button(ventana, text="Aceptar", 
                              command=lambda: callback(lista_proyectos.get(lista_proyectos.curselection()), proyectos, ventana))
    boton_aceptar.pack(pady=10, padx=20)

# Función para aceptar el proyecto seleccionado y proceder con la carga del documento
def aceptar_proyecto(proyecto_seleccionado, proyectos, ventana, entry_archivo, callback):
    """Asocia el proyecto seleccionado al documento y cierra la ventana."""
    for proyecto in proyectos:
        if proyecto[1] == proyecto_seleccionado:
            proyecto_id = proyecto[0]
            break
    ventana.destroy()  # Cerrar la ventana
    callback(proyecto_id)  # Llamar al callback con el ID del proyecto

# Función para cargar el documento seleccionado
def cargar_documento(entry_archivo, proyecto_id, frame_visual):
    """Extrae el texto del PDF, lo muestra en el visualizador y permite la edición antes de guardarlo."""
    ruta_archivo = entry_archivo.get()

    if not ruta_archivo:
        messagebox.showerror("Error", "No se ha seleccionado ningún archivo.")
        return

    try:
        # Extraer el texto del PDF
        texto_pdf = extraer_texto_pdf(ruta_archivo)

        # Limpiar el visualizador derecho
        limpiar_visualizador(frame_visual)

        # Mostrar el texto extraído en un widget de texto para revisión
        texto_requisitos = tk.Text(frame_visual, wrap="word", height=20)
        texto_requisitos.insert(tk.END, texto_pdf)
        texto_requisitos.pack(pady=10, padx=10, fill="both", expand=True)

        # Botón "Guardar" para confirmar la edición y guardar
        boton_guardar = tk.Button(frame_visual, text="Guardar",
                                  command=lambda: guardar_requisitos_y_asociaciones(texto_requisitos.get("1.0", tk.END), ruta_archivo, proyecto_id, frame_visual))
        boton_guardar.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar el documento: {e}")

# Función para guardar los requisitos y asociar subsistemas
def guardar_requisitos_y_asociaciones(requisitos_editados, ruta_archivo, proyecto_id, frame_visual):
    """Guarda el documento, los requisitos, y luego asigna subsistemas."""
    try:
        # Guardar el documento y los requisitos
        documento_id = insertar_documento("Título del documento", "1.0", proyecto_id)
        insertar_requisito(documento_id, 1, requisitos_editados)

        messagebox.showinfo("Éxito", "Documento, requisitos y asociaciones guardados correctamente")
        
        # Asignar subsistemas al documento
        asignar_subsistemas_a_documento_y_mostrar_ventana(requisitos_editados, documento_id, frame_visual)

    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar los requisitos: {e}")

# Función para mostrar ventana de asignación de subsistemas
def asignar_subsistemas_a_documento_y_mostrar_ventana(texto_documento, documento_id, frame_visual):
    """Crea una ventana para mostrar los subsistemas sugeridos y asignarlos al documento."""
    subsistemas_sugeridos = asignar_subsistemas_a_documento(texto_documento)

    ventana_subsistemas = tk.Toplevel()
    ventana_subsistemas.title("Asignación de Subsistemas")
    ventana_subsistemas.geometry("400x300")

    tk.Label(ventana_subsistemas, text="Subsistemas sugeridos para el documento:").pack(pady=10)

    # Listbox para mostrar los subsistemas sugeridos
    lista_subsistemas = tk.Listbox(ventana_subsistemas, selectmode=tk.MULTIPLE, height=10)
    for subsistema in subsistemas_sugeridos:
        lista_subsistemas.insert(tk.END, subsistema)
    lista_subsistemas.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Botón para aceptar la asignación de subsistemas
    boton_aceptar = tk.Button(ventana_subsistemas, text="Aceptar", 
                              command=lambda: aceptar_asignacion_subsistemas(documento_id, lista_subsistemas, ventana_subsistemas))
    boton_aceptar.pack(pady=10)

# Función para aceptar y guardar las asignaciones de subsistemas
def aceptar_asignacion_subsistemas(documento_id, lista_subsistemas, ventana_subsistemas):
    """Guarda los subsistemas seleccionados para el documento."""
    seleccionados = lista_subsistemas.curselection()
    subsistemas_asignados = [lista_subsistemas.get(i) for i in seleccionados]

    # Aquí puedes guardar la relación subsistema-documento en la base de datos
    print(f"Subsistemas asignados al documento {documento_id}: {subsistemas_asignados}")

    ventana_subsistemas.destroy()  # Cerrar la ventana de asignación
