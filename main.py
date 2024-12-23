"""
Archivo: iniciar_aplicacion.py
Descripción: Este archivo inicia la aplicación de gestión de requisitos, verificando y creando
la base de datos si es necesario, y lanzando la interfaz gráfica de usuario.
Autor: Estíbalitz Díez
Fecha: 23/12/2024
Version: 2
"""

import os
import logging
import sys
from almacenamiento.db import crear_directorio_base, crear_tablas
from idiomas.selector_idioma import seleccionar_idioma
from interfaz.interfaz_principal import interfaz_principal

# Configuración del registro (logging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def iniciar_aplicacion():
    """
    Función principal para iniciar la aplicación.

    Este método realiza las siguientes tareas:
    1. Selección de idioma utilizando `selector_idioma`.
    2. Verificación de la existencia de la base de datos.
    3. Creación de las tablas necesarias si la base de datos no existe.
    4. Verificación y creación del directorio de almacenamiento.
    5. Inicio de la interfaz gráfica de usuario.

    Raises:
        Exception: En caso de errores críticos durante la inicialización.
    """
    try:
        # Selección del idioma
        logging.info("Seleccionando idioma para la aplicación...")
        traducciones = seleccionar_idioma()

        # Rutas absolutas
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
        db_path = os.path.join(base_dir, "BD_Requisitos.db")  # Ruta de la base de datos
        ruta_base = os.path.join(base_dir, "almacen")  # Ruta del directorio de almacenamiento

        # Verificar y crear la base de datos si no existe
        if not os.path.exists(db_path):
            logging.info("La base de datos no existe, creando tablas...")
            crear_tablas(db_path)
            
        # Verificar y crear el directorio de almacenamiento si no existe
        if not os.path.exists(ruta_base):
            logging.info("El directorio de almacenamiento no existe, creándolo...")
            crear_directorio_base(ruta_base)

        # Iniciar la interfaz gráfica de usuario
        logging.info("Iniciando la interfaz de usuario...")
        interfaz_principal(traducciones, db_path)

    except Exception as e:
        logging.error("Error al iniciar la aplicación: %s", e)
        raise  # Propagar el error para depuración

# Punto de entrada principal
if __name__ == "__main__":
    try:
        iniciar_aplicacion()
    except KeyboardInterrupt:
        logging.info("Aplicación cerrada por el usuario.")
        sys.exit(0)
