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
    #cursor.execute('SELECT * FROM Documentos')
    # Consulta con JOIN para obtener el nombre del proyecto
    cursor.execute('''
        SELECT Documentos.id, Documentos.titulo, Documentos.version, Ciudades.nombre 
        FROM Documentos 
        JOIN Ciudades ON Documentos.ciudad = Ciudades.id
    ''')

    documentos = cursor.fetchall()

    # Obtenemos los nombres de las columnas sin afectar la base de datos
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]

    # Añadimos los nombres de las columnas como la primera fila en la lista de documentos
    documentos = [nombres_columnas] + documentos
    conexion.close()

    return documentos

def obtener_documentos_filtrados(subsistema=None, proyecto=None, documento=None):
    """Devuelve los documentos filtrados por subsistema, proyecto o ambos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    query = "SELECT * FROM Documentos WHERE 1=1"
    params = []
    
    if subsistema:
        query += " AND subsistema_id = ?"
        params.append(subsistema)
    
    if proyecto:
        query += " AND ciudad_id = ?"
        params.append(proyecto)
    
    if documento:
        query += " AND titulo LIKE ?"
        params.append(f"%{documento}%")
    
    cursor.execute(query, params)
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
