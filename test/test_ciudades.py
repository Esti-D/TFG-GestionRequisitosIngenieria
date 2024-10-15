import unittest
import sqlite3
from interfaz.versiones_anteriores.func_ciudades import insertar_ciudad, obtener_ciudades, borrar_ciudad

def limpiar_tabla_ciudades(conexion):
    """
    Función para limpiar la tabla Ciudades en la base de datos real.
    Elimina todos los registros de la tabla Ciudades.
    """
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Ciudades')
    conexion.commit()

class TestCiudades(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para cada test.
        Limpia la tabla Ciudades antes de comenzar.
        """
        # Conectarse a la base de datos real
        self.conexion = sqlite3.connect('BD_Requisitos.db')
        limpiar_tabla_ciudades(self.conexion)

    def tearDown(self):
        """
        Limpieza posterior a cada test.
        Limpia la tabla Ciudades y cierra la conexión a la base de datos.
        """
        limpiar_tabla_ciudades(self.conexion)
        self.conexion.close()

    def test_insertar_ciudad(self):
        """
        Prueba que inserta varias ciudades y verifica que fueron insertadas correctamente.
        """
        # Insertar ciudades
        insertar_ciudad("Madrid")
        insertar_ciudad("Barcelona")
        insertar_ciudad("Valencia")

        # Obtener ciudades de la base de datos
        ciudades = obtener_ciudades()

        # Verificar que las ciudades insertadas están presentes
        nombres_esperados = ["Madrid", "Barcelona", "Valencia"]
        nombres_obtenidos = [ciudad[1] for ciudad in ciudades]
        self.assertEqual(set(nombres_obtenidos), set(nombres_esperados))

def test_borrar_ciudad(self):
    """
    Prueba que inserta y luego borra una ciudad, verificando que fue eliminada correctamente.
    """
    # Insertar ciudades
    insertar_ciudad("Madrid")
    insertar_ciudad("Barcelona")

    # Obtener ciudades y buscar el ID de "Madrid"
    ciudades = obtener_ciudades()
    print("Ciudades antes de borrar:", ciudades)  # Imprimir las ciudades y sus IDs
    self.assertEqual(len(ciudades), 2)

    # Buscar el ID de Madrid
    madrid_id = None
    for ciudad in ciudades:
        if ciudad[1] == "Madrid":
            madrid_id = ciudad[0]
            break

    self.assertIsNotNone(madrid_id, "No se encontró la ciudad Madrid en la base de datos.")

    # Borrar la ciudad "Madrid" usando su ID
    borrar_ciudad(madrid_id)

    # Verificar que "Madrid" ha sido eliminada
    ciudades_actualizadas = obtener_ciudades()
    nombres_obtenidos = [ciudad[1] for ciudad in ciudades_actualizadas]
    print("Ciudades después de borrar:", ciudades_actualizadas)  # Imprimir ciudades después de borrar
    self.assertNotIn("Madrid", nombres_obtenidos)



if __name__ == "__main__":
    unittest.main()
