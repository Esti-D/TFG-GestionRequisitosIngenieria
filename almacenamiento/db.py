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
    print(
        f"Conectando a la base de datos: {db_path}"
    )  # Mostrar la ruta de la base de datos.
    conexion = sqlite3.connect(db_path)  # Conectar a la base de datos especificada.
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
            version VARCHAR(3),
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
            FOREIGN KEY (documento_id) REFERENCES Documentos(id)
        );
        """
    )

    # Confirmar los cambios en la base de datos.
    conexion.commit()
    conexion.close()  # Cerrar la conexión con la base de datos.


# Llamar a la función para crear las tablas cuando se ejecute el archivo directamente.
if __name__ == "__main__":
    # Usar una base de datos de prueba si se ejecuta directamente este archivo.
    db_path = os.path.join(os.getcwd(), "BD_Requisitos.db")
    crear_tablas(db_path)
