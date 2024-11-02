import tkinter as tk
from tkinter import messagebox
import re
from extraccion.leer_pdf import extraer_texto_pdf
from almacenamiento.func_documentos import insertar_documento, obtener_iddocumento
from almacenamiento.func_requisitos import insertar_requisito
from interfaz.c_bloque_acciones_independientes.bloque_asignaciones import limpiar_visualizador
from .asignar_subsistemas import asignar_subsistemas_a_documento_y_mostrar_ventana

def cargar_documento(traducciones,entry_archivo, proyecto_id, frame_visual):
    """Extrae el texto del PDF, organiza capítulos y divide requisitos basados en los puntos y aparte."""
    ruta_archivo = entry_archivo.get()

    titulo_documento = ruta_archivo.split("/")[-1]  # Obtener solo el nombre del archivo de la ruta

    if not ruta_archivo:
        messagebox.showerror(traducciones["M_Error"], traducciones["M_No_se_ha_seleccionado_ningún_archivo"])
        return

    try:
        texto_pdf = extraer_texto_pdf(ruta_archivo)
        if not texto_pdf:
            messagebox.showerror(traducciones["M_Error"],traducciones["M_No_se_pudo_extraer_texto_del_PDF"])
            return

        limpiar_visualizador(frame_visual)

        capitulos = re.split(r'(?=\d+\.\s)', texto_pdf)
        lista_req_cap = []
        contenido = ""
        capitulo_actual= None

        for capitulo in capitulos:
            capitulo = capitulo.strip()
            if not capitulo:
                continue

            match_capitulo = re.match(r'^(\d+)\.\s+(.+)', capitulo, re.DOTALL)
            if match_capitulo:
                capitulo_actual = match_capitulo.group(1)
                texto_capitulo = match_capitulo.group(2)

                contenido += f"{traducciones["T_CAPITULO"]} {capitulo_actual} :\n"
                requisitos = re.split(r'(?<=\.)\s*\n(?=[A-Z])', texto_capitulo)
                id_requisito = 1

                for requisito in requisitos:
                    if requisito.strip():
                        texto_requisito = requisito.strip()
                        lista_req_cap.append((capitulo_actual, texto_requisito))
                        contenido += f"{traducciones["T_REQUISITO"]} {id_requisito}: {texto_requisito}\n"
                        id_requisito += 1

            contenido += "\n"

        if contenido:
            texto_requisitos_visualizador = tk.Text(frame_visual, wrap="word", height=20)
            texto_requisitos_visualizador.insert(tk.END, contenido)
            texto_requisitos_visualizador.pack(pady=10, padx=10, fill="both", expand=True)
        else:
            messagebox.showerror(traducciones["M_Error"], traducciones["M_No_se_pudo_encontrar_ningún_capítulo_o_requisito_en_el_documento"])

        boton_guardar = tk.Button(frame_visual, text=traducciones["B_GUARDAR"], 
                                  command=lambda: guardar_requisitos_y_asociaciones(traducciones,titulo_documento, 
                                                                                    lista_req_cap,                                                                                    
                                                                                    texto_requisitos_visualizador.get("1.0", tk.END), 
                                                                                    ruta_archivo, proyecto_id, frame_visual))
        boton_guardar.pack(pady=10)

    except Exception as e:
        print(f"{traducciones["M_Error_al_cargar_el_documento"]} {e}")
        messagebox.showerror(traducciones["M_Error"], f"{traducciones["M_Error_al_cargar_el_documento"]} {e}")

def guardar_requisitos_y_asociaciones(traducciones,titulo_documento, lista_req_cap, requisitos_editados, ruta_archivo, proyecto_id, frame_visual):
    """Guarda el documento, los requisitos, y luego asigna subsistemas."""
    try:
        
        insertar_documento(titulo_documento, "1.0", proyecto_id)
        documento_id = obtener_iddocumento(titulo_documento, proyecto_id)
        
        print("verifico el nuemro de documento id:************ ",documento_id)
        print("Lista de capítulos:", lista_req_cap)
        
        # Iterar sobre ambas listas de forma paralela
        for capitulo, texto_requisito in lista_req_cap:
           
            # Guardar cada requisito con su capítulo asociado
            insertar_requisito(capitulo, texto_requisito, documento_id)

        #insertar_requisito( 1, requisitos_editados,documento_id)
        messagebox.showinfo(traducciones["M_Exito"], traducciones["M_Documentos,requisitos_y_asociaciones_guardados_correctamente"])
        print("verifico el numero de documento id:************ ",documento_id)
        asignar_subsistemas_a_documento_y_mostrar_ventana(traducciones,requisitos_editados, documento_id, frame_visual)

    except Exception as e:
        messagebox.showerror (traducciones["M_Error"], f"{traducciones["M_Error_al_guardar_los_requisitos"]}{e}") 
