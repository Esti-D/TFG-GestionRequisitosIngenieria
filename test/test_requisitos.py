import sys
import os
import sqlite3

# Añadir la ruta del directorio principal del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos las funciones desde la carpeta almacenamiento
from almacenamiento.func_requisitos import insertar_requisito, obtener_requisitos, borrar_requisito

# Función para borrar todos los datos de la tabla 'Requisitos' (sin eliminar la tabla) y resetear el AUTOINCREMENT
def limpiar_tabla_requisitos():
    conexion = sqlite3.connect('BD_Requisitos.db')
    cursor = conexion.cursor()
    # Eliminar todos los registros de la tabla Requisitos
    cursor.execute('DELETE FROM Requisitos')
    # Reiniciar el contador de AUTOINCREMENT
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="Requisitos"')
    conexion.commit()
    conexion.close()

# Borrar los registros existentes antes de empezar el test y reiniciar el ID
print("Limpiando la tabla 'Requisitos' antes de empezar el test...")
limpiar_tabla_requisitos()

# Prueba 1: Insertar requisitos
print("Insertando requisitos...")
insertar_requisito(2, "Requisito de Seguridad", 1)  # Suponemos que el documento con ID 1 existe
insertar_requisito(3, "Requisito de Rendimiento", 2)  # Suponemos que el documento con ID 2 existe

# Prueba 2: Consultar los requisitos
print("\nConsultando todos los requisitos...")
requisitos = obtener_requisitos()
print(requisitos)

# Prueba 3: Borrar un requisito (por ejemplo, el requisito con
