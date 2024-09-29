import sqlite3

# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect('BD_Requisitos.db')

# Insertar una ciudad
def insertar_ciudad(nombre_ciudad):
    """Inserta una nueva ciudad en la tabla Ciudades."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO Ciudades (nombre) VALUES (?)', (nombre_ciudad,))
    conexion.commit()
    conexion.close()

# Consultar todas las ciudades
def obtener_ciudades():
    """Devuelve todas las ciudades en la tabla Ciudades."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Ciudades')
    ciudades = cursor.fetchall()
    conexion.close()
    return ciudades

#Consultar ciudades/proyectos filtradass
def obtener_ciudades_filtradas(subsistema=None, proyecto=None, documento=None):
    """Devuelve las ciudades filtrados por subsistema, documento o ambos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    query = "SELECT * FROM Ciudades WHERE 1=1"
    params = []
    
    if subsistema:
        query += " AND subsistema_id = ?"
        params.append(subsistema)
    
    if proyecto:
        query += " AND ciudad_id = ?"
        params.append(proyecto)
    
    if documento:
        query += " AND titulo LIKE ?"
        params.append(f"%{documento}%")
    
    cursor.execute(query, params)
    proyecto = cursor.fetchall()
    conexion.close()
    return proyecto

# Eliminar una ciudad
def borrar_ciudad(ciudad_id):
    """Elimina una ciudad por su ID."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Ciudades WHERE id = ?', (ciudad_id,))
    conexion.commit()
    conexion.close()
