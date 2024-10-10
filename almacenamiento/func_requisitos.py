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
    # Obtenemos los nombres de las columnas sin afectar la base de datos
    nombres_columnas = [descripcion[0].upper() for descripcion in cursor.description]

    # Añadimos los nombres de las columnas como la primera fila en la lista de documentos
    requisitos = [nombres_columnas] + requisitos

    conexion.close()
    return requisitos

def obtener_requisitos_filtrados(subsistema=None, proyecto=None, documento=None):
    """Devuelve los documentos filtrados por subsistema, proyecto o ambos."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    query = "SELECT * FROM Requisitos WHERE 1=1"
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
