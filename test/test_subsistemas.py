import sys
import os
import sqlite3

# Añadir la ruta del directorio principal del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos las funciones desde la carpeta almacenamiento
from almacenamiento.func_subsistemas import insertar_subsistema, obtener_subsistemas, borrar_subsistema

# Función para borrar todos los datos de la tabla 'Subsistemas' (sin eliminar la tabla) y resetear el AUTOINCREMENT
def limpiar_tabla_subsistemas():
    conexion = sqlite3.connect('BD_Requisitos.db')
    cursor = conexion.cursor()
    # Eliminar todos los registros de la tabla Subsistemas
    cursor.execute('DELETE FROM Subsistemas')
    # Reiniciar el contador de AUTOINCREMENT
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="Subsistemas"')
    conexion.commit()
    conexion.close()

# Borrar los registros existentes antes de empezar el test y reiniciar el ID
print("Limpiando la tabla 'Subsistemas' antes de empezar el test...")
limpiar_tabla_subsistemas()

# Prueba 1: Insertar subsistemas
print("Insertando subsistemas...")
insertar_subsistema("Energía")
insertar_subsistema("Comunicaciones")

# Prueba 2: Consultar los subsistemas
print("\nConsultando todos los subsistemas...")
subsistemas = obtener_subsistemas()
print(subsistemas)

# Prueba 3: Borrar un subsistema (por ejemplo, el subsistema con ID 1)
print("\nEliminando el subsistema con ID 1...")
borrar_subsistema(1)

# Consultar de nuevo para verificar que fue eliminado
print("\nConsultando subsistemas después de eliminar...")
subsistemas_actualizados = obtener_subsistemas()
print(subsistemas_actualizados)

# Limpiar la tabla al final del test y reiniciar el ID
print("\nLimpiando la tabla 'Subsistemas' al final del test...")
limpiar_tabla_subsistemas()
