import sqlite3

# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect('BD_Requisitos.db')

# Insertar una proyecto
def insertar_proyecto(nombre_proyecto):
    """Inserta una nueva ciudad en la tabla Proyectos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO Proyectos (n_proyecto) VALUES (?)', (nombre_proyecto,))
    conexion.commit()
    conexion.close()

# Consultar todas las ciudades
def obtener_proyectos():
    """Devuelve todas las ciudades en la tabla Proyectos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Proyectos')
    proyectos = cursor.fetchall()

    # Obtenemos los nombres de las columnas sin afectar la base de datos
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]

    # Añadimos los nombres de las columnas como la primera fila en la lista de documentos
    proyectos = [nombres_columnas] + proyectos
    conexion.close()
    return proyectos

#Consultar ciudades/proyectos filtradass
def obtener_proyectos_filtradas(subsistema=None, proyecto=None, documento=None):
    """Devuelve las proyectos filtrados por subsistema, documento o ambos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    query = "SELECT * FROM Proyectos WHERE 1=1"
    params = []
    
    if subsistema:
        query += " AND subsistema_id = ?"
        params.append(subsistema)
    
    if proyecto:
        query += " AND proyecto_id = ?"
        params.append(proyecto)
    
    if documento:
        query += " AND titulo LIKE ?"
        params.append(f"%{documento}%")
    
    cursor.execute(query, params)
    proyecto = cursor.fetchall()
    conexion.close()
    return proyecto

# Eliminar una proyecto
def borrar_proyecto(proyecto_id):
    """Elimina una proyecto por su ID."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Proyectos WHERE id = ?', (proyecto_id,))
    conexion.commit()
    conexion.close()
