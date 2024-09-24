import sys
import os

# Añadir la ruta del directorio principal del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos las funciones desde la carpeta almacenamiento
from almacenamiento.func_ciudades import insertar_ciudad, obtener_ciudades, borrar_ciudad

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


