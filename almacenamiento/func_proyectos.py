"""
Archivo: func_proyectos.py
Descripción: Funciones para gestionar proyectos en la base de datos SQLite, incluyendo inserción,
consulta, filtrado y eliminación de proyectos.
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

# Insertar un proyecto
def insertar_proyecto(nombre_proyecto):
    """
    Inserta un nuevo proyecto en la tabla Proyectos.

    Args:
        nombre_proyecto (str): Nombre del proyecto que se desea insertar.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO Proyectos (n_proyecto) VALUES (?)", (nombre_proyecto,))

    conexion.commit()
    conexion.close()

# Consultar todos los proyectos
def obtener_proyectos():
    """
    Devuelve todos los proyectos almacenados en la tabla Proyectos.

    Returns:
        list: Lista de proyectos, incluyendo los nombres de columnas como primera fila.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Proyectos")
    proyectos = cursor.fetchall()

    # Agregar nombres de columnas como encabezados
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    proyectos = [nombres_columnas] + proyectos

    conexion.close()
    return proyectos

# Consultar proyectos filtrados
def obtener_proyectos_filtrados(subsistemaid=None, proyectoid=None, documentoid=None):
    """
    Devuelve los proyectos filtrados por subsistema, documento o ambos.

    Args:
        subsistemaid (int, optional): ID del subsistema para filtrar. Default es None.
        proyectoid (int, optional): ID del proyecto para filtrar. Default es None.
        documentoid (int, optional): ID del documento para filtrar. Default es None.

    Returns:
        list: Lista de proyectos filtrados, incluyendo los nombres de columnas como primera fila.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    query = """
    SELECT DISTINCT p.id, p.n_proyecto
    FROM Proyectos p
    JOIN Documentos d ON p.id = d.id_proyecto
    JOIN Asociacion_Documento_Subsistema ads ON d.id = ads.documento_id
    WHERE 1=1
    """
    params = []

    # Agregar filtros según los parámetros proporcionados
    if documentoid:
        query += " AND d.id = ?"
        params.append(documentoid)

    if subsistemaid:
        query += " AND ads.subsistema_id = ?"
        params.append(subsistemaid)

    # Ejecutar la consulta
    cursor.execute(query, params)
    proyectos = cursor.fetchall()

    # Agregar nombres de columnas como encabezados
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    proyectos = [nombres_columnas] + proyectos

    conexion.close()
    return proyectos

# Eliminar un proyecto
def borrar_proyecto(proyecto_id):
    """
    Elimina un proyecto de la tabla Proyectos basado en su ID.

    Args:
        proyecto_id (int): ID del proyecto que se desea eliminar.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Proyectos WHERE id = ?", (proyecto_id,))

    conexion.commit()
    conexion.close()

# Obtener el ID de un proyecto
def obtener_id_proyecto(nombre_proyecto):
    """
    Devuelve el ID de un proyecto dado su nombre.

    Args:
        nombre_proyecto (str): Nombre del proyecto.

    Returns:
        int or None: ID del proyecto si existe, de lo contrario None.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM Proyectos WHERE n_proyecto = ?", (nombre_proyecto,))
    resultado = cursor.fetchone()

    conexion.close()
    return resultado[0] if resultado else None
