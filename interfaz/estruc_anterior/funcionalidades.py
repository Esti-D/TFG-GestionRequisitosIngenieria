import tkinter as tk
from tkinter import filedialog
import os

def limpiar_fondo(frame_visual):
    for widget in frame_visual.winfo_children():
        widget.destroy()

def seleccionar_pdf(entry_archivo):
    filepath = filedialog.askopenfilename(
        title="Selecciona un archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if filepath:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, filepath)

def ejecutar_extraccion(entry_archivo, frame_visual):
    filepath = entry_archivo.get()
    if filepath:
        limpiar_fondo(frame_visual)
        label_archivo = tk.Label(frame_visual, text=f"Extrayendo del archivo: {os.path.basename(filepath)}", bg="white", font=("Arial", 12))
        label_archivo.pack(pady=20)
    else:
        print("No se ha seleccionado ningún archivo.")
