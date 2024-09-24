import sqlite3

# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect('BD_Requisitos.db')

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
