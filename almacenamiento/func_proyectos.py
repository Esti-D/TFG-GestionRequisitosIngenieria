import sqlite3


# Conectar a la base de datos
def conectar_db():
    """
    Establece una conexión con la base de datos SQLite.

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    return sqlite3.connect("BD_Requisitos.db")


# Insertar una proyecto
def insertar_proyecto(nombre_proyecto):
    """
    Inserta un nuevo proyecto en la tabla Proyectos.

    Args:
        nombre_proyecto (str): Nombre del proyecto que se desea insertar.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Inserta el nombre del proyecto en la tabla Proyectos.
    cursor.execute("INSERT INTO Proyectos (n_proyecto) VALUES (?)", (nombre_proyecto,))

    conexion.commit()
    conexion.close()


# Consultar todas las ciudades
def obtener_proyectos():
    """
    Devuelve todos los proyectos almacenados en la tabla Proyectos.

    Returns:
        list: Lista de proyectos incluyendo los nombres de columnas como primera fila.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Ejecuta una consulta para obtener todos los proyectos en la tabla Proyectos.
    cursor.execute("SELECT * FROM Proyectos")
    proyectos = cursor.fetchall()

    # Incluye los nombres de las columnas como encabezados.
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

    # Consulta base para obtener proyectos filtrados.
    query = """
    SELECT DISTINCT p.id, p.n_proyecto
    FROM Proyectos p
    JOIN Documentos d ON p.id = d.id_proyecto
    JOIN Asociacion_Documento_Subsistema ads ON d.id = ads.documento_id
    WHERE 1=1
    """
    params = []

    # Agregar filtros según los parámetros proporcionados.
    if documentoid:
        query += " AND d.id = ?"
        params.append(documentoid)

    if subsistemaid:
        query += " AND ads.subsistema_id = ?"
        params.append(subsistemaid)

    # Depuración: Imprime la consulta generada y los parámetros usados.
    print("Consulta SQL generada:", query)
    print("Parámetros de consulta:", params)

    # Ejecuta la consulta con los parámetros.
    cursor.execute(query, params)
    proyectos = cursor.fetchall()

    # Incluye los nombres de las columnas como encabezados.
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    proyectos = [nombres_columnas] + proyectos

    conexion.close()
    return proyectos


# Eliminar una proyecto
def borrar_proyecto(proyecto_id):
    """
    Elimina un proyecto de la tabla Proyectos basado en su ID.

    Args:
        proyecto_id (int): ID del proyecto que se desea eliminar.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Elimina el proyecto con el ID proporcionado.
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

    # Busca el ID del proyecto con el nombre proporcionado.
    cursor.execute("SELECT id FROM Proyectos WHERE n_proyecto = ?", (nombre_proyecto,))
    resultado = cursor.fetchone()

    conexion.close()
    return resultado[0] if resultado else None
