import sqlite3

# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect('BD_Requisitos.db')

# Insertar un requisito
def insertar_requisito(capitulo, requisito, documento_id):
    """Inserta un nuevo requisito en la tabla Requisitos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO Requisitos (capitulo, requisito, documento_id) VALUES (?, ?, ?)', 
                   (capitulo, requisito, documento_id))
    conexion.commit()
    conexion.close()

# Consultar todos los requisitos
def obtener_requisitos():
    """Devuelve todos los requisitos en la tabla Requisitos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Requisitos')
    requisitos = cursor.fetchall()
    conexion.close()
    return requisitos

# Eliminar un requisito
def borrar_requisito(requisito_id):
    """Elimina un requisito por su ID."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Requisitos WHERE id = ?', (requisito_id,))
    conexion.commit()
    conexion.close()
