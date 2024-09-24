import sys
import os
import sqlite3

# Añadir la ruta del directorio principal del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos las funciones desde la carpeta almacenamiento
from almacenamiento.func_relaciones import insertar_relacion_documento_subsistema, obtener_subsistemas_por_documento, obtener_documentos_por_subsistema, borrar_relacion_documento_subsistema

# Función para borrar todos los datos de la tabla de relaciones (sin eliminar la tabla)
def limpiar_tabla_relaciones():
    conexion = sqlite3.connect('BD_Requisitos.db')
    cursor = conexion.cursor()
    # Eliminar todos los registros de la tabla de relaciones
    cursor.execute('DELETE FROM Asociacion_Documento_Subsistema')
    conexion.commit()
    conexion.close()

# Borrar los registros existentes antes de empezar el test
print("Limpiando la tabla 'Asociacion_Documento_Subsistema' antes de empezar el test...")
limpiar_tabla_relaciones()

# Prueba 1: Insertar relaciones entre documentos y subsistemas
print("Insertando relaciones entre documentos y subsistemas...")
insertar_relacion_documento_subsistema(1, 1)  # Suponemos que el documento con ID 1 y el subsistema con ID 1 existen
insertar_relacion_documento_subsistema(1, 2)  # Suponemos que el subsistema con ID 2 existe

# Prueba 2: Consultar subsistemas asociados a un documento
print("\nConsultando subsistemas asociados al documento con ID 1...")
subsistemas = obtener_subsistemas_por_documento(1)
print(subsistemas)

# Prueba 3: Borrar una relación
print("\nEliminando la relación entre el documento con ID 1 y el subsistema con ID 1...")
borrar_relacion_documento_subsistema(1, 1)

# Consultar de nuevo para verificar que la relación fue eliminada
print("\nConsultando subsistemas asociados al documento con ID 1 después de eliminar...")
subsistemas_actualizados = obtener_subsistemas_por_documento(1)
print(subsistemas_actualizados)

# Limpiar la tabla de relaciones al final del test
print("\nLimpiando la tabla 'Asociacion_Documento_Subsistema' al final del test...")
limpiar_tabla_relaciones()
