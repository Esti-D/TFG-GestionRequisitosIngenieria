import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog # Para abrir el explorador de archivos
from extraccion.leer_pdf import extraer_texto_pdf
from almacenamiento. func_documentos import insertar_documento
from almacenamiento.func_requisitos import insertar_requisito
from almacenamiento.func_ciudades import obtener_ciudades  


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

#Función para abrir el explorador y seleccionar un archivo PDF
def seleccionar_archivo(entry_archivo):
   
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if archivo:
        entry_archivo.delete(0, tk.END) #limpiar el cuadro de texto
        entry_archivo.insert(0,archivo) # mostrar la ruta del archivo seleccionado
 
 #función para seleccionar una ciudad/proyecto al documento antes de cargarlo
def ventana_seleccionar_proyecto(callback):
    ventana = tk.Toplevel()
    ventana.title("Seleccionar Proyecto")
    
    #ajustar tamaño venta 
    ventana.geometry("400x300")

    proyectos = obtener_ciudades()  # Obtener lista de proyectos de la base de datos
   
   # Crear Listbox para mostrar directamente los proyectos
    lista_proyectos = tk.Listbox(ventana, height=10)  # Mostrar hasta 10 proyectos visibles
    for proyecto in proyectos:
        lista_proyectos.insert(tk.END, proyecto[1])  # Insertar solo el nombre del proyecto

    lista_proyectos.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)  # Ajustar a toda la ventana

    # Botón para aceptar la selección y llamar a la función callback
    boton_aceptar = tk.Button(ventana, text="Aceptar", 
                              command=lambda: callback(lista_proyectos.get(lista_proyectos.curselection()), proyectos, ventana))
    boton_aceptar.pack(pady=10, padx=20)

# Aceptar la selección del proyecto
def aceptar_proyecto(proyecto_seleccionado, proyectos, ventana, entry_archivo, callback):
    for proyecto in proyectos:
        if proyecto[1] == proyecto_seleccionado:
            proyecto_id = proyecto[0]
            break

    ventana.destroy()

    # Llamar al callback que pasa el proyecto_id a cargar_documento
    callback(proyecto_id)
   
def cargar_documento(entry_archivo,proyecto_id):
    #obtener la ruta del archivo
    ruta_archivo = entry_archivo.get()
    print(f"Ruta del archivo seleccionada: {ruta_archivo}") #mesnaje de  depuración

    if not ruta_archivo:
        messagebox.showerror("Error", "No se ha selecionado ningún archivo.")
        return
    try:
        #extraer el texto del archivo PDf
        print("Extrayendo texto del pdf..")
        texto_pdf = extraer_texto_pdf(ruta_archivo)
        print("texto extraido correctamente")

        # funcion insertar documetno
        print("insertando documento e nla base de datos..")
        documento_id= insertar_documento("Titulo del documento","1.0",ciudad_id=1)
        print(f"Documento insertado con ID: {documento_id}")

        print("insertando requisitos..")
        insertar_requisito(documento_id, 1, texto_pdf)
        print("requisitos insertados correctamente")

        messagebox.showinfo("Exito","Documento cargado correctamente")

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar el documento: {e}")


