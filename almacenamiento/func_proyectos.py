import sqlite3


# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect("BD_Requisitos.db")


# Insertar una proyecto
def insertar_proyecto(nombre_proyecto):
    """Inserta una nueva ciudad en la tabla Proyectos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Proyectos (n_proyecto) VALUES (?)", (nombre_proyecto,))
    conexion.commit()
    conexion.close()


# Consultar todas las ciudades
def obtener_proyectos():
    """Devuelve todas las ciudades en la tabla Proyectos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Proyectos")
    proyectos = cursor.fetchall()

    # Obtenemos los nombres de las columnas sin afectar la base de datos
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    # Añadimos los nombres de las columnas como la primera fila en la lista de documentos
    proyectos = [nombres_columnas] + proyectos

    conexion.close()
    return proyectos


# Consultar ciudades/proyectos filtradass
def obtener_proyectos_filtrados(subsistemaid=None, proyectoid=None, documentoid=None):
    """Devuelve las proyectos filtrados por subsistema, documento o ambos."""
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Base de la consulta
    query = """
    SELECT DISTINCT p.id, p.n_proyecto
    FROM Proyectos p
    JOIN Documentos d ON p.id = d.id_proyecto
    JOIN Asociacion_Documento_Subsistema ads ON d.id = ads.documento_id
    WHERE 1=1
    """
    params = []

    # Agregar filtro por documento si está presente
    if documentoid:
        query += " AND d.id = ?"
        params.append(documentoid)

    # Agregar filtro por subsistema si está presente
    if subsistemaid:
        query += " AND ads.subsistema_id = ?"
        params.append(subsistemaid)

    # Imprimir la consulta y los parámetros para debugging
    print("Consulta SQL generada:", query)
    print("Parámetros de consulta:", params)

    cursor.execute(query, params)
    proyectos = cursor.fetchall()

    # Obtenemos los nombres de las columnas sin afectar la base de datos
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    # Añadimos los nombres de las columnas como la primera fila en la lista de documentos
    proyectos = [nombres_columnas] + proyectos

    conexion.close()
    return proyectos


# Eliminar una proyecto
def borrar_proyecto(proyecto_id):
    """Elimina una proyecto por su ID."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Proyectos WHERE id = ?", (proyecto_id,))
    conexion.commit()
    conexion.close()


def obtener_id_proyecto(nombre_proyecto):
    """Devuelve el ID del subsistema dado su nombre."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM Proyectos WHERE n_proyecto = ?", (nombre_proyecto,))
    resultado = cursor.fetchone()
    conexion.close()

    return resultado[0] if resultado else None
