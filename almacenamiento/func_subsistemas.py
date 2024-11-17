import sqlite3
import os


# Conectar a la base de datos
def conectar_db():
    """
    Establece una conexión con la base de datos SQLite.

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    # Obtener la ruta absoluta de la base de datos
    db_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "BD_Requisitos.db"
    )
    print(
        f"Conectando a la base de datos en: {db_path}"
    )  # Imprimir la ruta de la base de datos para depuración
    return sqlite3.connect(db_path)


# Insertar un subsistema
def insertar_subsistema(nombre_subsistema):
    """
    Inserta un nuevo subsistema en la tabla Subsistemas.

    Args:
        nombre_subsistema (str): Nombre del subsistema a insertar.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Inserta el subsistema en la tabla
    cursor.execute("INSERT INTO Subsistemas (nombre) VALUES (?)", (nombre_subsistema,))

    conexion.commit()
    conexion.close()


# Consultar todos los subsistemas
def obtener_subsistemas():
    """
    Devuelve todos los subsistemas almacenados en la tabla Subsistemas.

    Returns:
        list: Lista de subsistemas, incluyendo los nombres de columnas como encabezados.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Consulta para obtener todos los subsistemas
    cursor.execute("SELECT * FROM Subsistemas")
    subsistemas = cursor.fetchall()

    # Incluye los nombres de las columnas como encabezados
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    subsistemas = [nombres_columnas] + subsistemas

    conexion.close()
    return subsistemas


# Consultar subsistemas filtrados
def obtener_subsistemas_filtrados(subsistemaid=None, proyectoid=None, documentoid=None):
    """
    Devuelve los subsistemas filtrados por proyecto, documento o ambos.

    Args:
        subsistemaid (int, optional): ID del subsistema para filtrar. Default es None.
        proyectoid (int, optional): ID del proyecto para filtrar. Default es None.
        documentoid (int, optional): ID del documento para filtrar. Default es None.

    Returns:
        list: Lista de subsistemas filtrados, incluyendo encabezados de columnas.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Consulta base para filtrar subsistemas
    query = """
    SELECT DISTINCT s.id, s.nombre
    FROM Subsistemas s
    JOIN Asociacion_Documento_Subsistema ads ON s.id = ads.subsistema_id
    JOIN Documentos d ON ads.documento_id = d.id
    WHERE 1=1
    """
    params = []

    # Agregar filtro por documento si está presente
    if documentoid:
        query += " AND d.id = ?"
        params.append(documentoid)

    # Agregar filtro por proyecto si está presente
    if proyectoid:
        query += " AND d.id_proyecto = ?"
        params.append(proyectoid)

    # Imprimir consulta y parámetros para depuración
    print("Consulta SQL generada:", query)
    print("Parámetros de consulta:", params)

    # Ejecutar la consulta con los parámetros proporcionados
    cursor.execute(query, params)
    subsistemas = cursor.fetchall()

    # Incluye los nombres de las columnas como encabezados
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    subsistemas = [nombres_columnas] + subsistemas

    conexion.close()
    return subsistemas


# Eliminar un subsistema
def borrar_subsistema(subsistema_id):
    """
    Elimina un subsistema de la tabla Subsistemas basado en su ID.

    Args:
        subsistema_id (int): ID del subsistema que se desea eliminar.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Elimina el subsistema con el ID proporcionado
    cursor.execute("DELETE FROM Subsistemas WHERE id = ?", (subsistema_id,))

    conexion.commit()
    conexion.close()


# Obtener el ID de un subsistema
def obtener_id_subsistema(nombre_subsistema):
    """
    Devuelve el ID de un subsistema dado su nombre.

    Args:
        nombre_subsistema (str): Nombre del subsistema.

    Returns:
        int or None: ID del subsistema si existe, de lo contrario None.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Busca el ID del subsistema con el nombre proporcionado
    cursor.execute("SELECT id FROM Subsistemas WHERE nombre = ?", (nombre_subsistema,))
    resultado = cursor.fetchone()

    conexion.close()
    return resultado[0] if resultado else None
