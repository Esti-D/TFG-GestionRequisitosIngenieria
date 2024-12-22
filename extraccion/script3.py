
import tkinter as tk
from tkinter import messagebox
import re
import os
from extraccion.leer_pdf import extraer_contenido_pdf, extraer_texto_pdf
from almacenamiento.func_documentos import insertar_documento, obtener_iddocumento
from almacenamiento.func_requisitos import insertar_requisito
from interfaz.a_bloque_load.cargar_documento import guardar_requisitos_completos_y_asociaciones
from interfaz.c_bloque_acciones_independientes.bloque_asignaciones import (
    limpiar_visualizador,
)

# HOY 24 NPOVIVEMBRE
import fitz
import re
import os
import fitz  # PyMuPDF
import re

from collections import Counter
def detectar_estructura_capitulos_pdf_mejorado(ruta_pdf):
    """
    Detecta automáticamente la estructura de los capítulos en un PDF, filtrando índices y listas.

    Args:
        ruta_pdf (str): Ruta al archivo PDF.

    Returns:
        dict: Información sobre la estructura de los capítulos.
              Ejemplo:
              {
                  "patron": r"^\d+\.\s",
                  "ejemplos": ["1. Introduction", "2. Methodology"],
                  "frecuencia": 10
              }
    """
    lineas_candidatas = []
    coincidencias = []

    try:
        with fitz.open(ruta_pdf) as pdf_document:
            for pagina in pdf_document:
                bloques = pagina.get_text("blocks")  # Obtener bloques de texto con coordenadas
                for bloque in bloques:
                    _, _, _, _, texto = bloque
                    texto = texto.strip()
                    if texto:
                        lineas_candidatas.append(texto)

    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
        return None

    # Heurísticas para filtrar líneas candidatas
    for linea in lineas_candidatas:
        if len(linea) < 5 or len(linea.split()) > 12:  # Filtrar líneas demasiado cortas o largas
            continue
        if linea.strip().isdigit():  # Evitar líneas que son solo números
            continue
        if re.match(r".+\s+\d+$", linea):  # Evitar índices con números de página al final
            continue

        # Buscar patrones numéricos y simbólicos al inicio
        match = re.match(r"^(\d+|[IVXLCDM]+)(\.|\)|-| )\s+.*", linea)
        if match:
            coincidencias.append(match.group(0))  # Guardar línea que coincide con patrón

    # Contar las frecuencias de los formatos detectados
    patrones_detectados = [re.match(r"^(\d+|[IVXLCDM]+)(\.|\)|-| )", linea).group(0) for linea in coincidencias]
    frecuencia_patrones = Counter(patrones_detectados)

    if not frecuencia_patrones:
        return None  # No se detectaron patrones

    # Elegir el patrón más frecuente
    patron_principal = max(frecuencia_patrones, key=frecuencia_patrones.get)
    ejemplos = [linea for linea in coincidencias if linea.startswith(patron_principal)]

    # Crear un patrón regex dinámico
    patron_regex = rf"^{re.escape(patron_principal)}\s+"

    return {
        "patron": patron_regex,
        "ejemplos": ejemplos[:5],  # Mostrar hasta 5 ejemplos
        "frecuencia": frecuencia_patrones[patron_principal],
    }

def cargar_documento_completo(traducciones, entry_archivo, proyecto_id, frame_visual):
    ruta_archivo = entry_archivo.get()

    titulo_documento = ruta_archivo.split("/")[
        -1
    ]

    if not ruta_archivo:
        messagebox.showerror(
            traducciones["M_Error"],
            traducciones["M_No_se_ha_seleccionado_ningún_archivo"],
        )
        return

    try:
        # Detectar estructura de capítulos
        estructura = detectar_estructura_capitulos_pdf_mejorado(ruta_archivo)
        if not estructura:
            messagebox.showerror(
                traducciones["M_Error"],
                traducciones["M_No_se_pudo_detectar_estructura_de_capítulos"],
            )
            return

        patron_capitulo = estructura["patron"]

        # Extraer texto completo
        texto_pdf = extraer_contenido_pdf(ruta_archivo, proyecto_id)

        # Dividir el texto en capítulos usando el patrón detectado
        capitulos = re.split(patron_capitulo, texto_pdf)
        
        if not capitulos:
            messagebox.showerror(
                traducciones["M_Error"],
                traducciones["M_No_se_encontraron_capítulos_en_el_documento"],
            )
            return

        lista_req_cap = []  # Lista para almacenar los capítulos y requisitos extraídos.
        contenido = ""  # Contenido a mostrar en el área de texto.

        for idx, capitulo in enumerate(capitulos, start=1):
            capitulo = capitulo.strip()
            if not capitulo:
                continue
                
            contenido += f"{traducciones['T_CAPITULO']} {idx} :\n"

            # Dividir el texto del capítulo en requisitos, basados en puntos y aparte.
            requisitos = re.split(r"(?<=\.)\s*\n(?=[A-Z])", capitulo)
            id_requisito = 1

            for requisito in requisitos:
                if requisito.strip():
                    texto_requisito = requisito.strip()  # Eliminar espacios.
                    lista_req_cap.append((idx, texto_requisito))
                    contenido += f"{traducciones['T_REQUISITO']} {id_requisito}: {texto_requisito}\n"
                    id_requisito += 1

            contenido += "\n"

        # Mostrar el contenido extraído en un widget de texto dentro del frame.
        if contenido:
            texto_requisitos_visualizador = tk.Text(
                frame_visual, wrap="word", height=20
            )
            texto_requisitos_visualizador.insert(tk.END, contenido)
            texto_requisitos_visualizador.pack(
                pady=10, padx=10, fill="both", expand=True
            )
        else:
            # Mostrar mensaje de error si no se encontraron capítulos ni requisitos.
            messagebox.showerror(
                traducciones["M_Error"],
                traducciones[
                    "M_No_se_pudo_encontrar_ningún_capítulo_o_requisito_en_el_documento"
                ],
            )

        # Crear un botón para guardar los datos extraídos.
        boton_guardar = tk.Button(
            frame_visual,
            text=traducciones["B_GUARDAR"],
            command=lambda: guardar_requisitos_completos_y_asociaciones(
                traducciones,
                titulo_documento,
                lista_req_cap,
                texto_requisitos_visualizador.get("1.0", tk.END),
                ruta_archivo,
                proyecto_id,
                frame_visual,
            ),
        )
        boton_guardar.pack(pady=10)

    except Exception as e:
        # Capturar y mostrar errores inesperados.
        print(f"{traducciones['M_Error_al_cargar_el_documento']} {e}")
        messagebox.showerror(
            traducciones["M_Error"],
            f"{traducciones['M_Error_al_cargar_el_documento']} {e}",
        )

