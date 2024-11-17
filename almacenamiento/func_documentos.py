import sqlite3


# Conectar a la base de datos
def conectar_db():
    """
    Establece la conexión con la base de datos SQLite.

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    return sqlite3.connect("BD_Requisitos.db")


# Insertar un documento
def insertar_documento(titulo, version, proyecto_id):
    """
    Inserta un nuevo documento en la tabla Documentos.

    Args:
        titulo (str): Título del documento.
        version (str): Versión del documento.
        proyecto_id (int): ID del proyecto asociado al documento.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Insertar el documento en la tabla Documentos
    cursor.execute(
        "INSERT INTO Documentos (titulo, version, id_proyecto) VALUES (?, ?, ?)",
        (titulo, version, proyecto_id),
    )

    conexion.commit()
    conexion.close()


# Obtener el ID de un documento
def obtener_iddocumento(titulo, proyecto_id):
    """
    Obtiene el ID de un documento en función de su título y proyecto asociado.

    Args:
        titulo (str): Título del documento.
        proyecto_id (int): ID del proyecto asociado.

    Returns:
        int or None: ID del documento, o None si no se encuentra.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Consultar el ID del documento
    cursor.execute(
        "SELECT id FROM Documentos WHERE titulo = ? and id_proyecto = ?",
        (titulo, proyecto_id),
    )
    id_documento = cursor.fetchone()
    conexion.close()

    return id_documento[0] if id_documento else None


# Consultar todos los documentos
def obtener_documentos():
    """
    Devuelve todos los documentos de la base de datos, incluyendo sus proyectos asociados.

    Returns:
        list: Lista de documentos, incluyendo encabezados de columnas.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Consultar todos los documentos con sus proyectos asociados
    cursor.execute(
        """
        SELECT Documentos.id, Documentos.titulo, Documentos.version, Proyectos.n_proyecto 
        FROM Documentos 
        JOIN Proyectos ON Documentos.id_proyecto = Proyectos.id
        """
    )

    documentos = cursor.fetchall()

    # Obtener los nombres de las columnas para incluir como encabezados
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    documentos = [nombres_columnas] + documentos

    conexion.close()
    return documentos


# Consultar documentos filtrados
def obtener_documentos_filtrados(subsistema=None, proyecto=None, documento=None):
    """
    Devuelve documentos filtrados por subsistema, proyecto o título del documento.

    Args:
        subsistema (str, optional): Nombre del subsistema. Default es None.
        proyecto (str, optional): Nombre del proyecto. Default es None.
        documento (str, optional): Título del documento. Default es None.

    Returns:
        list: Lista de documentos filtrados, incluyendo encabezados de columnas.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Imprimir valores iniciales para debugging
    print(
        f"Parámetros recibidos - Proyecto: {proyecto}, Documento: {documento}, Subsistema: {subsistema}"
    )

    # Limpiar espacios y manejar valores None
    if proyecto:
        proyecto = proyecto.strip()
    if documento:
        documento = documento.strip()
    if subsistema:
        subsistema = subsistema.strip()

    # Imprimir valores después de limpiar
    print(
        f"Parámetros después de limpiar - Proyecto: {proyecto}, Documento: {documento}, Subsistema: {subsistema}"
    )

    # Base de la consulta
    query = """
    SELECT d.id, d.titulo, d.version, p.n_proyecto
    FROM Documentos d
    JOIN Proyectos p ON d.id_proyecto = p.id
    WHERE 1=1
    """
    params = []

    # Agregar filtros condicionales
    if proyecto:
        query += " AND p.n_proyecto = ?"
        params.append(proyecto)

    if documento:
        query += " AND d.titulo = ?"
        params.append(documento)

    if subsistema:
        query += """
        AND d.id IN (
            SELECT ads.documento_id 
            FROM Asociacion_Documento_Subsistema ads
            JOIN Subsistemas s ON ads.subsistema_id = s.id 
            WHERE s.nombre = ?
        )
        """
        params.append(subsistema)

    # Imprimir consulta final y parámetros
    print("Consulta SQL generada:", query)
    print("Parámetros de consulta:", params)

    # Ejecutar la consulta
    cursor.execute(query, params)
    documentos = cursor.fetchall()

    # Obtener nombres de columnas
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    documentos = [nombres_columnas] + documentos

    conexion.close()
    return documentos


# Eliminar un documento
def borrar_documento(documento_id):
    """
    Elimina un documento de la base de datos basado en su ID.

    Args:
        documento_id (int): ID del documento a eliminar.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Eliminar el documento por su ID
    cursor.execute("DELETE FROM Documentos WHERE id = ?", (documento_id,))
    conexion.commit()
    conexion.close()
