import tkinter as tk
from asignacion.asignacion_subsistemas import asignar_subsistemas_a_documento

def asignar_subsistemas_a_documento_y_mostrar_ventana(texto_documento, documento_id, frame_visual):
    """Crea una ventana para mostrar los subsistemas sugeridos y asignarlos al documento."""
    subsistemas_sugeridos = asignar_subsistemas_a_documento(texto_documento)
    
    ventana_subsistemas = tk.Toplevel()
    ventana_subsistemas.title("Asignación de Subsistemas")
    ventana_subsistemas.geometry("400x300")

    tk.Label(ventana_subsistemas, text="Subsistemas sugeridos para el documento:").pack(pady=10)

    lista_subsistemas = tk.Listbox(ventana_subsistemas, selectmode=tk.MULTIPLE, height=10)
    for subsistema in subsistemas_sugeridos:
        lista_subsistemas.insert(tk.END, subsistema)
    lista_subsistemas.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    boton_aceptar = tk.Button(ventana_subsistemas, text="Aceptar", 
                              command=lambda: aceptar_asignacion_subsistemas(documento_id, lista_subsistemas, ventana_subsistemas))
    boton_aceptar.pack(pady=10)

def aceptar_asignacion_subsistemas(documento_id, lista_subsistemas, ventana_subsistemas):
    """Guarda los subsistemas seleccionados para el documento."""
    seleccionados = lista_subsistemas.curselection()
    subsistemas_asignados = [lista_subsistemas.get(i) for i in seleccionados]

    print(f"Subsistemas asignados al documento {documento_id}: {subsistemas_asignados}")
    ventana_subsistemas.destroy()
