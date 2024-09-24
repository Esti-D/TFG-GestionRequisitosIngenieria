import sqlite3

# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect('BD_Requisitos.db')

# Insertar un documento
def insertar_documento(titulo, version, ciudad_id):
    """Inserta un nuevo documento en la tabla Documentos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO Documentos (titulo, version, ciudad) VALUES (?, ?, ?)', 
                   (titulo, version, ciudad_id))
    conexion.commit()
    conexion.close()

# Consultar todos los documentos
def obtener_documentos():
    """Devuelve todos los documentos en la tabla Documentos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Documentos')
    documentos = cursor.fetchall()
    conexion.close()
    return documentos

# Eliminar un documento
def borrar_documento(documento_id):
    """Elimina un documento por su ID."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Documentos WHERE id = ?', (documento_id,))
    conexion.commit()
    conexion.close()
