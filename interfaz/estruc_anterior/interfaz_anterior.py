import tkinter as tk
from PIL import Image, ImageTk
import os
from interfaz_componentes import crear_boton_load, crear_campos_filtros, crear_botones_adicionales

# Crear ventana principal
ventana = tk.Tk()
ventana.title("RM Requirements Management")
ventana.state('zoomed')  # Maximiza la ventana

# Incluir el logo en la barra del software
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_icono = os.path.join(ruta_base, "logo_reducido.ico")  # Reemplaza "logo.ico" con el nombre correcto de tu archivo de icono
ventana.iconbitmap(ruta_icono)  # Añadir el icono a la ventana

# Crear frames
frame_funcionalidades = tk.Frame(ventana, bg="lightgray", padx=20, pady=20)
frame_funcionalidades.grid(row=0, column=0, sticky="nsew")

frame_visual = tk.Frame(ventana, bg="white")
frame_visual.grid(row=0, column=1, sticky="nsew")

# Configurar el grid de la ventana
ventana.grid_columnconfigure(0, weight=1, uniform="group1")
ventana.grid_columnconfigure(1, weight=1, uniform="group1")
ventana.grid_rowconfigure(0, weight=1)

# Cargar imagen de fondo para la parte visual (derecha)
ruta_fondo = os.path.join(ruta_base, "logofondo.png")  # Reemplaza "logofondo.png" por el nombre correcto de tu imagen
imagen_fondo = Image.open(ruta_fondo)
imagen_fondo = imagen_fondo.resize((600, 400))  # Ajusta el tamaño según sea necesario
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)
label_fondo = tk.Label(frame_visual, image=imagen_fondo_tk, bg="white")
label_fondo.pack(expand=True)

# Llamar a las funciones para crear los componentes de la interfaz
crear_boton_load(frame_funcionalidades)  # Función para el botón LOAD y selección de archivos
crear_campos_filtros(frame_funcionalidades)  # Función para los filtros de consulta y casillas de selección
crear_botones_adicionales(frame_funcionalidades)  # Función para los botones adicionales (Proyecto, Subsistema, etc.)

# Ejecutar el mainloop de la ventana
ventana.mainloop()
