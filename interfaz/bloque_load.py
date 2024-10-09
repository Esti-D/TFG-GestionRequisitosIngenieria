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
import re

def cargar_documento(entry_archivo, proyecto_id, frame_visual):
    """Extrae el texto del PDF, organiza capítulos y divide requisitos basados en los puntos y aparte."""
    ruta_archivo = entry_archivo.get()

    # Extraer el nombre del archivo PDF directamente desde la ruta
    titulo_documento = ruta_archivo.split("/")[-1]  # Obtener solo el nombre del archivo de la ruta
    
    if not ruta_archivo:
        messagebox.showerror("Error", "No se ha seleccionado ningún archivo.")
        return

    try:
        # Extraer el texto del PDF
        texto_pdf = extraer_texto_pdf(ruta_archivo)

        # Verificar si se extrajo correctamente el texto
        if not texto_pdf:
            messagebox.showerror("Error", "No se pudo extraer texto del PDF.")
            return

        # Limpiar el visualizador antes de mostrar el nuevo contenido
        limpiar_visualizador(frame_visual)

        # Dividir el texto en capítulos basados en números seguidos de puntos
        capitulos = re.split(r'(?=\d+\.\s)', texto_pdf)  # Detectar capítulos basados en números seguidos de un punto

        contenido = ""  # Aquí almacenamos el contenido que se mostrará en el visor

        # Recorremos los capítulos para extraer los requisitos
        for capitulo in capitulos:
            capitulo = capitulo.strip()  # Limpiar espacios en blanco

            # Asegurarse de que no estamos en un bloque vacío
            if not capitulo:
                continue

            # Detectar el número del capítulo
            match_capitulo = re.match(r'^(\d+)\.\s+(.+)', capitulo, re.DOTALL)
            if match_capitulo:
                numero_capitulo = match_capitulo.group(1)  # Número del capítulo
                texto_capitulo = match_capitulo.group(2)  # Resto del capítulo

                contenido += f"Capítulo {numero_capitulo}:\n"

                # Dividir los párrafos en requisitos por punto y aparte (detectamos un punto, seguido de un salto de línea, seguido de mayúscula)
                requisitos = re.split(r'(?<=\.)\s*\n(?=[A-Z])', texto_capitulo)
                id_requisito = 1

                for requisito in requisitos:
                    requisito = requisito.strip()  # Limpiar espacios en blanco
                    if requisito:
                        contenido += f"Requisito {id_requisito}: {requisito}\n"
                        id_requisito += 1

            contenido += "\n"  # Separar capítulos visualmente

        # Mostrar el contenido estructurado en el visualizador para que el usuario lo pueda editar
        if contenido:
            texto_requisitos_visualizador = tk.Text(frame_visual, wrap="word", height=20)
            # Insertamos el contenido de capítulos y requisitos en el visor
            texto_requisitos_visualizador.insert(tk.END, contenido)
            texto_requisitos_visualizador.pack(pady=10, padx=10, fill="both", expand=True)
        else:
            messagebox.showerror("Error", "No se pudo encontrar ningún capítulo o requisito en el documento.")

        # Botón para guardar después de la revisión
        boton_guardar = tk.Button(frame_visual, text="Guardar", command=lambda: guardar_requisitos_y_asociaciones(titulo_documento,texto_requisitos_visualizador.get("1.0", tk.END),ruta_archivo, proyecto_id, frame_visual))
        boton_guardar.pack(pady=10)

    except Exception as e:
        print(f"Error al cargar el documento: {e}")  # Para depuración
        messagebox.showerror("Error", f"Error al cargar el documento: {e}")

# Función para guardar los requisitos y asociar subsistemas
def guardar_requisitos_y_asociaciones(titulo_documento, requisitos_editados, ruta_archivo, proyecto_id, frame_visual):
    """Guarda el documento, los requisitos, y luego asigna subsistemas."""
    try:
        # Guardar el documento y los requisitos
        documento_id = insertar_documento(titulo_documento, "1.0", proyecto_id)
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
