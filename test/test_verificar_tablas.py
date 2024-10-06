import sqlite3
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def listar_tablas():
    """
    Función para listar las tablas de la base de datos.
    Devuelve una lista con los nombres de las tablas.
    """
    try:
        conexion = sqlite3.connect('BD_Requisitos.db')
        cursor = conexion.cursor()

        # Consultar las tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        conexion.close()

        # Loguear las tablas encontradas
        logging.info(f"Tablas encontradas: {[tabla[0] for tabla in tablas]}")
        return [tabla[0] for tabla in tablas]

    except sqlite3.Error as e:
        logging.error(f"Error al listar las tablas: {e}")
        return []

def mostrar_contenido_tabla(tabla):
    """
    Función para mostrar el contenido de una tabla dada.
    """
    try:
        conexion = sqlite3.connect('BD_Requisitos.db')
        cursor = conexion.cursor()

        # Consultar el contenido de la tabla
        cursor.execute(f"SELECT * FROM {tabla}")
        contenido = cursor.fetchall()
        conexion.close()

        # Mostrar el contenido de la tabla
        if contenido:
            logging.info(f"Contenido de la tabla {tabla}:")
            for fila in contenido:
                logging.info(fila)
        else:
            logging.info(f"La tabla {tabla} está vacía.")

    except sqlite3.Error as e:
        logging.error(f"Error al obtener el contenido de la tabla {tabla}: {e}")

if __name__ == "__main__":
    # Listar las tablas y mostrar su contenido
    tablas = listar_tablas()
    
    if not tablas:
        logging.warning("No se encontraron tablas en la base de datos.")
    else:
        for tabla in tablas:
            mostrar_contenido_tabla(tabla)
