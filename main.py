import os
import logging
from almacenamiento.db import crear_tablas
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
        # Verificar si la base de datos ya existe
        if not os.path.exists('BD_Requisitos.db'):
            logging.info("La base de datos no existe, creando tablas...")
            crear_tablas()

        # Iniciar la interfaz gráfica
        logging.info("Iniciando la interfaz de usuario...")
        interfaz_principal()
        

    except Exception as e:
        logging.error(f"Error al iniciar la aplicación: {e}")
        raise

if __name__ == "__main__":
    iniciar_aplicacion()
