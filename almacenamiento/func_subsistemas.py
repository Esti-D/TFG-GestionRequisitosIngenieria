import sqlite3
import os


def conectar_db():
    # Obtener la ruta absoluta de la base de datos
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'BD_Requisitos.db')
    print(f"Conectando a la base de datos en: {db_path}")  # Esto imp
    return sqlite3.connect(db_path)

# Insertar un subsistema
def insertar_subsistema(nombre_subsistema):
    """Inserta un nuevo subsistema en la tabla Subsistemas."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO Subsistemas (nombre) VALUES (?)', (nombre_subsistema,))
    conexion.commit()
    conexion.close()

# Consultar todos los subsistemas
def obtener_subsistemas():
    """Devuelve todos los subsistemas en la tabla Subsistemas."""
    conexion = conectar_db()
  
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Subsistemas')
    subsistemas = cursor.fetchall()
    
    # Obtenemos los nombres de las columnas sin afectar la base de datos
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    # Añadimos los nombres de las columnas como la primera fila en la lista de documentos
    subsistemas = [nombres_columnas] + subsistemas

    conexion.close()
    return subsistemas

#Consultar subsistemas filtrados
def obtener_subsistemas_filtrados(subsistemaid=None, proyectoid=None, documentoid=None):
    
   
    """Devuelve los subsistemas filtrados por proyecto, documento o ambos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Base de la consulta
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

    # Imprimir la consulta y los parámetros para debugging
    print("Consulta SQL generada:", query)
    print("Parámetros de consulta:", params)
    
    cursor.execute(query, params)
    subsistemas = cursor.fetchall()
    
    # Obtenemos los nombres de las columnas sin afectar la base de datos
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]
    # Añadimos los nombres de las columnas como la primera fila en la lista de documentos
    subsistemas = [nombres_columnas] + subsistemas

    conexion.close()
    return subsistemas

# Eliminar un subsistema
def borrar_subsistema(subsistema_id):
    """Elimina un subsistema por su ID."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Subsistemas WHERE id = ?', (subsistema_id,))
    conexion.commit()
    conexion.close()

def obtener_id_subsistema(nombre_subsistema):
    """Devuelve el ID del subsistema dado su nombre."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM Subsistemas WHERE nombre = ?", (nombre_subsistema,))
    resultado = cursor.fetchone()
    conexion.close()
    
    return resultado[0] if resultado else None