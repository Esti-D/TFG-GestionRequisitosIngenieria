"""
Archivo: func_documentos.py
Descripción: Contiene funciones para gestionar documentos en la base de datos SQLite, 
incluyendo inserción, consulta, filtrado y eliminación de documentos.
Autor: Estíbalitz Díez
Fecha: 23/12/2024
Version: 2
"""

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
        version (int): Versión del documento.
        proyecto_id (int): ID del proyecto asociado al documento.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO Documentos (titulo, version, id_proyecto) VALUES (?, ?, ?)",
        (titulo, version, proyecto_id),
    )

    conexion.commit()
    conexion.close()

# Obtener el ID de un documento
def obtener_iddocumento(titulo, proyecto_id, version):
    """
    Obtiene el ID de un documento en función de su título, versión y proyecto asociado.

    Args:
        titulo (str): Título del documento.
        version (int): Versión del documento.
        proyecto_id (int): ID del proyecto asociado.

    Returns:
        int or None: ID del documento, o None si no se encuentra.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id FROM Documentos WHERE titulo = ? AND id_proyecto = ? AND version = ?",
        (titulo, proyecto_id, version),
    )
    id_documento = cursor.fetchone()
    conexion.close()

    return id_documento[0] if id_documento else None

# Obtener la última versión de un documento
def obtener_version(titulo, proyecto_id):
    """
    Obtiene la última versión de un documento en función de su título y proyecto asociado.

    Args:
        titulo (str): Título del documento.
        proyecto_id (int): ID del proyecto asociado.

    Returns:
        int or None: Última versión del documento como entero, o None si no se encuentra.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT MAX(version) FROM Documentos WHERE titulo = ? AND id_proyecto = ?",
        (titulo, proyecto_id),
    )
    version = cursor.fetchone()
    conexion.close()

    return int(version[0]) if version and version[0] else None

# Consultar todos los documentos
def obtener_documentos():
    """
    Devuelve todos los documentos de la base de datos, incluyendo sus proyectos asociados.

    Returns:
        list: Lista de documentos, incluyendo encabezados de columnas.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT Documentos.id, Documentos.titulo, Documentos.version, Proyectos.n_proyecto 
        FROM Documentos 
        JOIN Proyectos ON Documentos.id_proyecto = Proyectos.id
        """
    )

    documentos = cursor.fetchall()
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
        params.append(proyecto.strip())

    if documento:
        query += " AND d.titulo = ?"
        params.append(documento.strip())

    if subsistema:
        query += """
        AND d.id IN (
            SELECT ads.documento_id 
            FROM Asociacion_Documento_Subsistema ads
            JOIN Subsistemas s ON ads.subsistema_id = s.id 
            WHERE s.nombre = ?
        )
        """
        params.append(subsistema.strip())

    cursor.execute(query, params)
    documentos = cursor.fetchall()

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

    # Eliminar primero los requisitos asociados
    cursor.execute("DELETE FROM Requisitos WHERE documento_id = ?", (documento_id,))

    # Eliminar el documento por su ID
    cursor.execute("DELETE FROM Documentos WHERE id = ?", (documento_id,))

    conexion.commit()
    conexion.close()
