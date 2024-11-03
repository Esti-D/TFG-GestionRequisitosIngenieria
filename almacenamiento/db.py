import sqlite3
import os


def crear_tablas(db_path):
    """Función para crear las tablas necesarias en la base de datos."""
    print(
        f"Conectando a la base de datos: {db_path}"
    )  # Confirmar la ruta de la base de datos
    conexion = sqlite3.connect(
        db_path
    )  # Usar la ruta de la base de datos pasada como argumento
    cursor = conexion.cursor()

    # Crear tabla Proyectos
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Proyectos (
        id INTEGER PRIMARY KEY,
        n_proyecto VARCHAR(20) UNIQUE NOT NULL
    );
    """
    )

    # Crear tabla Documentos
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Documentos (
        id INTEGER PRIMARY KEY,
        titulo VARCHAR(130),
        version VARCHAR(3),
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        id_proyecto INTEGER NOT NULL,
        UNIQUE (titulo, version, id_proyecto),
        FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id)
    );
    """
    )

    # Crear tabla Subsistemas
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Subsistemas (
        id INTEGER PRIMARY KEY,
        nombre VARCHAR(50)
    );
    """
    )

    # Crear tabla de Asociación entre Documentos y Subsistemas
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

    # Crear tabla Requisitos
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Requisitos (
        id INTEGER PRIMARY KEY,
        capitulo INTEGER,
        requisito VARCHAR(1000),
        documento_id INTEGER,
        FOREIGN KEY (documento_id) REFERENCES Documentos(id)
    );
    """
    )

    conexion.commit()
    conexion.close()


# Llamar a la función para crear las tablas cuando se ejecute el archivo
if __name__ == "__main__":
    crear_tablas()
