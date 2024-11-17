"""
Este archivo inicia la aplicación de gestión de requisitos.  
Verifica y crea la base de datos, y luego lanza la interfaz gráfica.  
"""

import os
import logging
from almacenamiento.db import crear_tablas
from idiomas.selector_idioma import seleccionar_idioma
from interfaz.interfaz_principal import interfaz_principal

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def iniciar_aplicacion():
    """
    Función principal para iniciar la aplicación.

    Este método se encarga de verificar si la base de datos existe. Si no existe,
    se crean las tablas necesarias utilizando el módulo `almacenamiento.db`.
    Posteriormente, se inicializa la interfaz de usuario.

    Flujo principal:
        1. Selección de idioma mediante `selector_idioma`.
        2. Verificación de la existencia de la base de datos.
        3. Creación de tablas si la base de datos no existe.
        4. Inicio de la interfaz gráfica.

    Raises:
        Exception: En caso de errores críticos durante la inicialización.
    """
    try:
        # Seleccionar idioma para la aplicación y obtener traducciones.
        traducciones = seleccionar_idioma()

        # Obtener la ruta absoluta de la base de datos.
        db_path = os.path.join(os.path.dirname(__file__), "BD_Requisitos.db")

        # Verificar si la base de datos ya existe.
        if not os.path.exists(db_path):
            logging.info("La base de datos no existe, creando tablas...")
            crear_tablas(db_path)  # Crear las tablas solo si la base de datos no existe.

        # Iniciar la interfaz gráfica.
        logging.info("Iniciando la interfaz de usuario...")
        interfaz_principal(
            traducciones, db_path
        )  # Pasar la ruta de la base de datos a la interfaz.

    except Exception as e:
        # Manejo de errores críticos durante la inicialización.
        logging.error("Error al iniciar la aplicación: %s", e)
        raise  # Propagar el error para depuración.

# Punto de entrada principal para ejecutar la aplicación.
if __name__ == "__main__":
    iniciar_aplicacion()
