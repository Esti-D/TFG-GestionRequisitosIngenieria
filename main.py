"""
Este archivo inicia la aplicación de gestión de requisitos.  
Verifica y crea la base de datos, y luego lanza la interfaz gráfica.  
"""

import os
import logging
from almacenamiento.db import crear_directorio_base, crear_tablas
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
        4. Verificación y creación del directorio de almacenamiento.
        5. Inicio de la interfaz gráfica.

    Raises:
        Exception: En caso de errores críticos durante la inicialización.
    """
    try:
        # Seleccionar idioma para la aplicación y obtener traducciones.
        logging.info("Seleccionando idioma para la aplicación...")
        traducciones = seleccionar_idioma()

        # Definir rutas absolutas
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Ruta del directorio actual
        db_path = os.path.join(base_dir, "BD_Requisitos.db")  # Ruta para la base de datos
        ruta_base = os.path.join(base_dir, "almacen")  # Ruta para el almacenamiento

        # Verificar si la base de datos ya existe.
        if not os.path.exists(db_path):
            logging.info("La base de datos no existe, creando tablas...")
            crear_tablas(db_path)  # Crear las tablas solo si la base de datos no existe.
            
        if not os.path.exists(ruta_base):
            logging.info("El directorio de almacenamiento no existe, creándolo...")
            crear_directorio_base(ruta_base)     
            

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
