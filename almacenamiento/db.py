import sqlite3

def conectar_db():
    """Función para conectar a la base de datos."""
    conexion = sqlite3.connect('BD_Requisitos.db')  # Nombre del archivo de la base de datos
    return conexion

def crear_tablas():
    """Función para crear las tablas necesarias."""
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Crear tabla Ciudades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ciudades (
        id INTEGER PRIMARY KEY,
        nombre VARCHAR(20) UNIQUE NOT NULL
    );
    ''')

    # Crear tabla Documentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Documentos (
        id INTEGER PRIMARY KEY,
        titulo VARCHAR(130),
        version VARCHAR(3),
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        ciudad INTEGER NOT NULL,
        UNIQUE (titulo, version, ciudad),
        FOREIGN KEY (ciudad) REFERENCES Ciudades(id)
    );
    ''')

    # Crear tabla Subsistemas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Subsistemas (
        id INTEGER PRIMARY KEY,
        nombre VARCHAR(50)
    );
    ''')

    # Crear tabla de Asociación entre Documentos y Subsistemas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Asociacion_Documento_Subsistema (
        documento_id INTEGER,
        subsistema_id INTEGER,
        PRIMARY KEY (documento_id, subsistema_id),
        FOREIGN KEY (documento_id) REFERENCES Documentos(id),
        FOREIGN KEY (subsistema_id) REFERENCES Subsistemas(id)
    );
    ''')

    # Crear tabla Requisitos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Requisitos (
        id INTEGER PRIMARY KEY,
        capitulo INTEGER,
        requisito VARCHAR(1000),
        documento_id INTEGER,
        FOREIGN KEY (documento_id) REFERENCES Documentos(id)
    );
    ''')

    conexion.commit()
    conexion.close()

# Llamar a la función para crear las tablas cuando se ejecute el archivo
if __name__ == "__main__":
    crear_tablas()
