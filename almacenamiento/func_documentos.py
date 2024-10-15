import sqlite3

# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect('BD_Requisitos.db')

# Insertar un documento
def insertar_documento(titulo, version, proyecto_id):
    """Inserta un nuevo documento en la tabla Documentos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO Documentos (titulo, version, id_proyecto) VALUES (?, ?, ?)', 
                   (titulo, version, proyecto_id))
    conexion.commit()
    conexion.close()

# Consultar todos los documentos
def obtener_documentos():
    """Devuelve todos los documentos en la tabla Documentos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
  
    cursor.execute('''
        SELECT Documentos.id, Documentos.titulo, Documentos.version, Proyectos.n_proyecto 
        FROM Documentos 
        JOIN Proyectos ON Documentos.id_proyecto = Proyectos.id
    ''')

    documentos = cursor.fetchall()

    # Obtenemos los nombres de las columnas sin afectar la base de datos
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]

    # Añadimos los nombres de las columnas como la primera fila en la lista de documentos
    documentos = [nombres_columnas] + documentos
    conexion.close()

    return documentos

def obtener_documentos_filtrados(subsistema=None, proyecto=None, documento=None):
    """Devuelve los documentos filtrados por nombre de proyecto, título del documento o subsistema."""
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Imprimir los valores recibidos para debugging
    print(f"Parámetros recibidos - Proyecto: {proyecto}, Documento: {documento}, Subsistema: {subsistema}")

    # Asegurarnos de que los parámetros están limpios (quitar espacios y verificar None)
    if proyecto:
        proyecto = proyecto.strip()  # Eliminar espacios en blanco antes y después
    if documento:
        documento = documento.strip()
    if subsistema:
        subsistema = subsistema.strip()

    # Imprimir después de limpiar los parámetros
    print(f"Parámetros después de limpiar - Proyecto: {proyecto}, Documento: {documento}, Subsistema: {subsistema}")

    # Base de la consulta
    query = """
    SELECT d.id, d.titulo, d.version, p.n_proyecto
    FROM Documentos d
    JOIN Proyectos p ON d.id_proyecto = p.id
    WHERE 1=1
    """
    params = []

    # Agregar filtro por nombre de proyecto si está presente
    if proyecto:
        query += " AND p.n_proyecto = ?"
        params.append(proyecto)

    # Agregar filtro por título del documento si está presente
    if documento:
        query += " AND d.titulo = ?"
        params.append(documento)

    # Agregar filtro por subsistema si está presente
    if subsistema:
        query += """
        AND d.id IN (SELECT ads.documento_id FROM Asociacion_Documento_Subsistema ads
                     JOIN Subsistemas s ON ads.subsistema_id = s.id WHERE s.nombre = ?)
        """
        params.append(subsistema)


    # Ejecutar la consulta con los parámetros adecuados
    cursor.execute(query,params)
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
