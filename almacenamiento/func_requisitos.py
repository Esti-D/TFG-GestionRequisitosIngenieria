import sqlite3


# Conectar a la base de datos
def conectar_db():
    """
    Establece una conexión con la base de datos SQLite.

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    return sqlite3.connect("BD_Requisitos.db")


# Insertar un requisito
def insertar_requisito(capitulo, requisito, documento_id):
    """
    Inserta un nuevo requisito en la tabla Requisitos.

    Args:
        capitulo (int): Número del capítulo al que pertenece el requisito.
        requisito (str): Texto del requisito.
        documento_id (int): ID del documento asociado al requisito.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Inserta el requisito en la tabla Requisitos
    cursor.execute(
        "INSERT INTO Requisitos (capitulo, requisito, documento_id) VALUES (?, ?, ?)",
        (capitulo, requisito, documento_id),
    )

    conexion.commit()
    conexion.close()


# Consultar todos los requisitos
def obtener_requisitos():
    """
    Devuelve todos los requisitos almacenados en la tabla Requisitos.

    Returns:
        list: Lista de requisitos, incluyendo encabezados de columnas.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Consulta para obtener todos los requisitos
    cursor.execute(
        "SELECT Requisitos.id, Requisitos.capitulo, Requisitos.requisito, Requisitos.documento_id FROM Requisitos"
    )
    requisitos = cursor.fetchall()

    # Incluye los nombres de las columnas como encabezados
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    requisitos = [nombres_columnas] + requisitos

    conexion.close()
    return requisitos


# Consultar requisitos filtrados
def obtener_requisitos_filtrados(subsistema=None, proyecto=None, documento=None):
    """
    Devuelve los requisitos filtrados por subsistema, proyecto y/o documento.

    Args:
        subsistema (int, optional): ID del subsistema para filtrar. Default es None.
        proyecto (int, optional): ID del proyecto para filtrar. Default es None.
        documento (int, optional): ID del documento para filtrar. Default es None.

    Returns:
        list: Lista de requisitos filtrados, incluyendo encabezados de columnas.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Consulta base para filtrar requisitos
    query = """
    SELECT r.id, r.capitulo, r.requisito, r.documento_id
    FROM Requisitos r
    JOIN Documentos d ON r.documento_id = d.id
    JOIN Asociacion_Documento_Subsistema ads ON r.documento_id = ads.documento_id
    JOIN Subsistemas s ON ads.subsistema_id = s.id
    WHERE 1=1
    """
    params = []

    # Agregar filtro por subsistema si está presente
    if subsistema:
        query += " AND ads.subsistema_id =  ?"
        params.append(subsistema)

    # Agregar filtro por proyecto si está presente
    if proyecto:
        query += " AND d.id_proyecto =  ?"
        params.append(proyecto)

    # Agregar filtro por documento si está presente
    if documento:
        query += " AND d.id = ?"
        params.append(documento)

    # Depuración: Imprime la consulta generada y los parámetros usados
    print("Consulta SQL generada:", query)
    print("Parámetros de consulta:", params)

    # Ejecutar la consulta con los parámetros proporcionados
    cursor.execute(query, params)
    requisitos = cursor.fetchall()

    # Incluye los nombres de las columnas como encabezados
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    requisitos = [nombres_columnas] + requisitos

    conexion.close()
    return requisitos


# Eliminar un requisito
def borrar_requisito(requisito_id):
    """
    Elimina un requisito de la tabla Requisitos basado en su ID.

    Args:
        requisito_id (int): ID del requisito que se desea eliminar.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Elimina el requisito con el ID proporcionado
    cursor.execute("DELETE FROM Requisitos WHERE id = ?", (requisito_id,))

    conexion.commit()
    conexion.close()
