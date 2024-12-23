"""
Archivo: func_relaciones.py
Descripción: Funciones para gestionar las relaciones entre documentos y subsistemas en la base de datos SQLite.
Autor: Estíbalitz Díez
Fecha: 23/12/2024
Versión: 2
"""

import sqlite3

# Conectar a la base de datos
def conectar_db():
    """
    Establece una conexión con la base de datos SQLite.

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    return sqlite3.connect("BD_Requisitos.db")

# Insertar la relación entre Documento y Subsistema
def insertar_relacion_documento_subsistema(documento_id, subsistema_id):
    """
    Inserta una relación entre un documento y un subsistema en la base de datos.

    Args:
        documento_id (int): ID del documento.
        subsistema_id (int): ID del subsistema.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Inserta la relación en la tabla Asociacion_Documento_Subsistema
    cursor.execute(
        "INSERT INTO Asociacion_Documento_Subsistema (documento_id, subsistema_id) VALUES (?, ?)",
        (documento_id, subsistema_id),
    )

    conexion.commit()
    conexion.close()

# Consultar subsistemas por documento
def obtener_subsistemas_por_documento(documento_id):
    """
    Devuelve todos los subsistemas asociados a un documento.

    Args:
        documento_id (int): ID del documento.

    Returns:
        list: Lista de nombres de subsistemas asociados al documento.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Consulta para obtener los subsistemas asociados a un documento
    cursor.execute(
        """
        SELECT Subsistemas.nombre 
        FROM Subsistemas 
        INNER JOIN Asociacion_Documento_Subsistema 
        ON Subsistemas.id = Asociacion_Documento_Subsistema.subsistema_id 
        WHERE Asociacion_Documento_Subsistema.documento_id = ?
        """,
        (documento_id,),
    )
    subsistemas = cursor.fetchall()
    conexion.close()
    return subsistemas

# Consultar documentos por subsistema
def obtener_documentos_por_subsistema(subsistema_id):
    """
    Devuelve todos los documentos asociados a un subsistema.

    Args:
        subsistema_id (int): ID del subsistema.

    Returns:
        list: Lista de títulos de documentos asociados al subsistema.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Consulta para obtener los documentos asociados a un subsistema
    cursor.execute(
        """
        SELECT Documentos.titulo 
        FROM Documentos
        INNER JOIN Asociacion_Documento_Subsistema 
        ON Documentos.id = Asociacion_Documento_Subsistema.documento_id 
        WHERE Asociacion_Documento_Subsistema.subsistema_id = ?
        """,
        (subsistema_id,),
    )
    documentos = cursor.fetchall()
    conexion.close()
    return documentos

# Eliminar una relación entre Documento y Subsistema
def borrar_relacion_documento_subsistema(documento_id, subsistema_id):
    """
    Elimina una relación específica entre un documento y un subsistema.

    Args:
        documento_id (int): ID del documento.
        subsistema_id (int): ID del subsistema.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Elimina la relación de la tabla Asociacion_Documento_Subsistema
    cursor.execute(
        "DELETE FROM Asociacion_Documento_Subsistema WHERE documento_id = ? AND subsistema_id = ?",
        (documento_id, subsistema_id),
    )

    conexion.commit()
    conexion.close()

# Modificar la relación entre Documento y Subsistema
def modificar_relacion_documento_subsistema(documento_id, subsistema_id_viejo, subsistema_id_nuevo):
    """
    Modifica una relación entre un documento y un subsistema, reemplazando la antigua con una nueva.

    Args:
        documento_id (int): ID del documento.
        subsistema_id_viejo (int): ID del subsistema a eliminar.
        subsistema_id_nuevo (int): ID del subsistema a añadir.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Elimina la relación antigua
    cursor.execute(
        "DELETE FROM Asociacion_Documento_Subsistema WHERE documento_id = ? AND subsistema_id = ?",
        (documento_id, subsistema_id_viejo),
    )

    # Inserta la nueva relación
    cursor.execute(
        "INSERT INTO Asociacion_Documento_Subsistema (documento_id, subsistema_id) VALUES (?, ?)",
        (documento_id, subsistema_id_nuevo),
    )

    conexion.commit()
    conexion.close()

# Consultar todas las relaciones
def obtener_relaciones():
    """
    Devuelve todas las relaciones entre documentos y subsistemas.

    Returns:
        list: Lista de relaciones incluyendo los nombres de columnas como primera fila.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Consulta para obtener todas las relaciones
    cursor.execute("SELECT * FROM Asociacion_Documento_Subsistema")
    proyectos = cursor.fetchall()

    # Incluye los nombres de las columnas como encabezados
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    proyectos = [nombres_columnas] + proyectos

    conexion.close()
    return proyectos
