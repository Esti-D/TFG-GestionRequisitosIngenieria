"""
Archivo: db.py
Descripción: Contiene funciones para la creación de tablas en la base de datos SQLite
y la configuración del directorio base para el almacenamiento de requisitos, imágenes y tablas.
Autor: Estíbalitz Díez
Fecha: 23/12/2024
Version: 2
"""

import sqlite3
import os

def crear_tablas(db_path):
    """
    Crea las tablas necesarias en la base de datos SQLite.

    Args:
        db_path (str): Ruta completa al archivo de la base de datos.

    Tablas creadas:
        1. Proyectos: Almacena los proyectos gestionados.
        2. Documentos: Almacena los documentos asociados a proyectos.
        3. Subsistemas: Almacena los subsistemas definidos.
        4. Asociacion_Documento_Subsistema: Relaciona documentos con subsistemas.
        5. Requisitos: Almacena los requisitos extraídos de documentos.
    """
    print(f"Conectando a la base de datos: {db_path}")
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Crear tabla Proyectos: Gestiona los proyectos.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Proyectos (
            id INTEGER PRIMARY KEY,
            n_proyecto VARCHAR(20) UNIQUE NOT NULL
        );
        """
    )

    # Crear tabla Documentos: Gestiona documentos asociados a proyectos.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Documentos (
            id INTEGER PRIMARY KEY,
            titulo VARCHAR(130),
            version INTEGER,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            id_proyecto INTEGER NOT NULL,
            UNIQUE (titulo, version, id_proyecto),
            FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id)
        );
        """
    )

    # Crear tabla Subsistemas: Gestiona los subsistemas.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Subsistemas (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR(50)
        );
        """
    )

    # Crear tabla Asociacion_Documento_Subsistema: Relaciona documentos con subsistemas.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Asociacion_Documento_Subsistema (
            documento_id INTEGER,
            subsistema_id INTEGER,
            PRIMARY KEY (documento_id, subsistema_id),
            FOREIGN KEY (documento_id) REFERENCES Documentos(id),
            FOREIGN KEY (subsistema_id) REFERENCES Subsistemas(id)
        );
        """
    )

    # Crear tabla Requisitos: Gestiona los requisitos extraídos de documentos.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Requisitos (
            id INTEGER PRIMARY KEY,
            capitulo INTEGER,
            requisito VARCHAR(1000),
            documento_id INTEGER,
            FOREIGN KEY (documento_id) REFERENCES Documentos(id) ON DELETE CASCADE
        );
        """
    )

    # Confirmar los cambios en la base de datos.
    conexion.commit()
    conexion.close()  # Cerrar la conexión con la base de datos.


def crear_directorio_base(ruta_base):
    """
    Crea el directorio base en la ubicación especificada para almacenar reqisitos imagenes y tablas.

    Args:
        ruta_base (str): Ruta completa del directorio base.
    """
        
    if not os.path.exists(ruta_base):
        os.makedirs(ruta_base)
        print(f"Directorio base creado en: {ruta_base}")
    else:
        print(f"Directorio base ya existe en: {ruta_base}")


# Llamar a la función para crear las tablas cuando se ejecute el archivo directamente.
if __name__ == "__main__":
    """
    Ejecución directa del archivo:
    - Crea una base de datos de prueba.
    - Configura el directorio base de almacenamiento.
    """
    ruta_principal = os.getcwd()

    # Definir rutas
    db_path = os.path.join(ruta_principal, "BD_Requisitos.db")
    ruta_base = os.path.join(ruta_principal, "almacen")

    # Crear tablas y directorio
    crear_tablas(db_path)
    crear_directorio_base(ruta_base)
