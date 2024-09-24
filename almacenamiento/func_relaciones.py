import sqlite3

# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect('BD_Requisitos.db')

# Insertar la relación entre Documento y Subsistema
def insertar_relacion_documento_subsistema(documento_id, subsistema_id):
    """Inserta la relación entre un documento y un subsistema."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO Asociacion_Documento_Subsistema (documento_id, subsistema_id) VALUES (?, ?)',
                   (documento_id, subsistema_id))
    conexion.commit()
    conexion.close()

# Consultar subsistemas por documento
def obtener_subsistemas_por_documento(documento_id):
    """Devuelve todos los subsistemas asociados a un documento."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('''
    SELECT Subsistemas.nombre 
    FROM Subsistemas 
    INNER JOIN Asociacion_Documento_Subsistema 
    ON Subsistemas.id = Asociacion_Documento_Subsistema.subsistema_id 
    WHERE Asociacion_Documento_Subsistema.documento_id = ?
    ''', (documento_id,))
    subsistemas = cursor.fetchall()
    conexion.close()
    return subsistemas

# Consultar documentos por subsistema
def obtener_documentos_por_subsistema(subsistema_id):
    """Devuelve todos los documentos asociados a un subsistema."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('''
    SELECT Documentos.titulo 
    FROM Documentos
    INNER JOIN Asociacion_Documento_Subsistema 
    ON Documentos.id = Asociacion_Documento_Subsistema.documento_id 
    WHERE Asociacion_Documento_Subsistema.subsistema_id = ?
    ''', (subsistema_id,))
    documentos = cursor.fetchall()
    conexion.close()
    return documentos

# Eliminar una relación entre Documento y Subsistema
def borrar_relacion_documento_subsistema(documento_id, subsistema_id):
    """Elimina la relación entre un documento y un subsistema."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Asociacion_Documento_Subsistema WHERE documento_id = ? AND subsistema_id = ?',
                   (documento_id, subsistema_id))
    conexion.commit()
    conexion.close()

# Modificar la relación entre Documento y Subsistema
def modificar_relacion_documento_subsistema(documento_id, subsistema_id_viejo, subsistema_id_nuevo):
    """Modifica la relación entre un documento y un subsistema."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    # Eliminar la relación vieja
    cursor.execute('DELETE FROM Asociacion_Documento_Subsistema WHERE documento_id = ? AND subsistema_id = ?',
                   (documento_id, subsistema_id_viejo))
    # Insertar la relación nueva
    cursor.execute('INSERT INTO Asociacion_Documento_Subsistema (documento_id, subsistema_id) VALUES (?, ?)',
                   (documento_id, subsistema_id_nuevo))
    conexion.commit()
    conexion.close()
