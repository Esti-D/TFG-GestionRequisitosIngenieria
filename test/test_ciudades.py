import sys
import os
import sqlite3

# Añadir la ruta del directorio principal del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos las funciones desde la carpeta almacenamiento
from almacenamiento.func_ciudades import insertar_ciudad, obtener_ciudades, borrar_ciudad

# Función para borrar todos los datos de la tabla 'Ciudades' (sin eliminar la tabla) y resetear el AUTOINCREMENT
def limpiar_tabla_ciudades():
    conexion = sqlite3.connect('BD_Requisitos.db')
    cursor = conexion.cursor()
    # Eliminar todos los registros de la tabla Ciudades
    cursor.execute('DELETE FROM Ciudades')
    # Reiniciar el contador de AUTOINCREMENT
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="Ciudades"')
    conexion.commit()
    conexion.close()

# Borrar los registros existentes antes de empezar el test y reiniciar el ID
print("Limpiando la tabla 'Ciudades' antes de empezar el test...")
limpiar_tabla_ciudades()

# Prueba 1: Insertar una ciudad
print("Insertando ciudades...")
insertar_ciudad("Madrid")
insertar_ciudad("Barcelona")
insertar_ciudad("Valencia")

# Prueba 2: Consultar las ciudades
print("\nConsultando todas las ciudades...")
ciudades = obtener_ciudades()
print(ciudades)

# Prueba 3: Borrar una ciudad (por ejemplo, Madrid, que tiene ID 1)
print("\nEliminando la ciudad con ID 1 (Madrid)...")
borrar_ciudad(1)

# Consultar de nuevo para verificar que fue eliminada
print("\nConsultando ciudades después de eliminar...")
ciudades_actualizadas = obtener_ciudades()
print(ciudades_actualizadas)

# Limpiar la tabla al final del test y reiniciar el ID
print("\nLimpiando la tabla 'Ciudades' al final del test...")
limpiar_tabla_ciudades()
