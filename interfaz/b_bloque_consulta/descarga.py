import csv
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk


def es_numero(valor):
    """Comprueba si el valor es un número."""
    try:
        float(valor)
        return True
    except ValueError:
        return False


def descargar_csv(traducciones, frame_visual):
    """Exporta el contenido visible de frame_visual a un archivo CSV."""

    # Solicitar nombre y ubicación para guardar el archivo
    archivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title=(traducciones["B_Guardar_como"]),
    )

    if not archivo:
        return  # Salir si no se selecciona un archivo

    datos_a_guardar = []

    # Función auxiliar para extraer datos de widgets anidados
    def extraer_datos(widget):
        if isinstance(widget, tk.Label):
            datos_a_guardar.append(widget.cget("text"))
        elif isinstance(widget, tk.Listbox):
            listbox_data = [widget.get(idx) for idx in range(widget.size())]
            datos_a_guardar.extend(listbox_data)
        elif isinstance(widget, tk.Text):
            texto = widget.get("1.0", tk.END).strip()
            if texto:
                datos_a_guardar.append(texto)
        elif isinstance(widget, ttk.Treeview):
            headers = [col for col in widget["columns"]]
            datos_a_guardar.extend(headers)
            for item in widget.get_children():
                row_data = widget.item(item)["values"]
                datos_a_guardar.extend(row_data)
        elif isinstance(widget, (tk.Frame, tk.Canvas)):
            for child in widget.winfo_children():
                extraer_datos(child)

    # Llamar a la función auxiliar en cada widget dentro de `frame_visual`
    for widget in frame_visual.winfo_children():
        extraer_datos(widget)

    # Determinar el número de columnas
    datos_filas = []
    fila_actual = []
    num_columnas = None

    for elemento in datos_a_guardar:
        if es_numero(elemento) and num_columnas is None:
            num_columnas = len(fila_actual)  # Define columnas con elementos hasta "1"
            datos_filas.append(
                fila_actual
            )  # Agrega la primera fila (sin incluir el "1")
            fila_actual = [elemento]  # Comienza la siguiente fila con el "1"
        else:
            fila_actual.append(elemento)

        if num_columnas and len(fila_actual) == num_columnas:
            datos_filas.append(fila_actual)
            fila_actual = []

    # Guardar la última fila si está incompleta
    if fila_actual:
        datos_filas.append(fila_actual)

    # Guardar datos en CSV si hay datos capturados
    if datos_filas:
        try:
            with open(archivo, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(datos_filas)
            messagebox.showinfo(
                traducciones["M_Exito"],
                traducciones["M_Archivo_CSV_guardado_correctamente"],
            )
        except Exception as e:
            messagebox.showerror(
                traducciones["M_Error"],
                f"{traducciones['M_No_se_pudo_guardar_el_archivo_CSV']}: {e}",
            )
    else:
        messagebox.showinfo(
            traducciones["M_Info"], traducciones["M_No_hay_datos_para_guardar"]
        )
