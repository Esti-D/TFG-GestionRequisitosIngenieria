import sys
import os
import sqlite3

# Añadir la ruta del directorio principal del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos las funciones desde la carpeta almacenamiento
from almacenamiento.func_documentos import insertar_documento, obtener_documentos, borrar_documento

# Función para borrar todos los datos de la tabla 'Documentos' (sin eliminar la tabla) y resetear el AUTOINCREMENT
def limpiar_tabla_documentos():
    conexion = sqlite3.connect('BD_Requisitos.db')
    cursor = conexion.cursor()
    # Eliminar todos los registros de la tabla Documentos
    cursor.execute('DELETE FROM Documentos')
    # Reiniciar el contador de AUTOINCREMENT
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="Documentos"')
    conexion.commit()
    conexion.close()

# Borrar los registros existentes antes de empezar el test y reiniciar el ID
print("Limpiando la tabla 'Documentos' antes de empezar el test...")
limpiar_tabla_documentos()

# Prueba 1: Insertar un documento
print("Insertando documentos...")
insertar_documento("Plan de Ingeniería", "1.0", 1)  # Suponemos que la ciudad con ID 1 existe
insertar_documento("Especificaciones Técnicas", "1.2", 2)  # Suponemos que la ciudad con ID 2 existe

# Prueba 2: Consultar los documentos
print("\nConsultando todos los documentos...")
documentos = obtener_documentos()
print(documentos)

# Prueba 3: Borrar un documento (por ejemplo, el documento con ID 1)
print("\nEliminando el documento con ID 1...")
borrar_documento(1)

# Consultar de nuevo para verificar que fue eliminado
print("\nConsultando documentos después de eliminar...")
documentos_actualizados = obtener_documentos()
print(documentos_actualizados)

# Limpiar la tabla al final del test y reiniciar el ID
print("\nLimpiando la tabla 'Documentos' al final del test...")
limpiar_tabla_documentos()
