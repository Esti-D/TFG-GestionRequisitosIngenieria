import os
import logging
import tkinter as tk
from almacenamiento.db import crear_tablas
from idiomas.selector_idioma import seleccionar_idioma
from interfaz.interfaz_principal import interfaz_principal


# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def iniciar_aplicacion():
    """
    Función principal para iniciar la aplicación.
    Verifica si la base de datos existe, si no, crea las tablas necesarias.
    Luego, inicia la interfaz de usuario.
    """
    try:

        # Llamada a `seleccion`, pasando la ventana como `frame_visual`
        traducciones=seleccionar_idioma()

        # Obtener la ruta absoluta de la base de datos
        db_path = os.path.join(os.path.dirname(__file__), 'BD_Requisitos.db')

        # Verificar si la base de datos ya existe
        if not os.path.exists(db_path):
            logging.info("La base de datos no existe, creando tablas...")
            crear_tablas(db_path)  # Crear las tabals solo si la bas de datos no existe

        # Iniciar la interfaz gráfica
        logging.info("Iniciando la interfaz de usuario...")
        interfaz_principal(traducciones,db_path)  # Pasar la ruta de la base de datos a la interfaz
        
    except Exception as e:
        logging.error(f"Error al iniciar la aplicación: {e}")
        raise # Propagar el error para obtener más detalles en la depuración

if __name__ == "__main__":
    iniciar_aplicacion()
