import unittest
import sqlite3
from almacenamiento.func_subsistemas import insertar_subsistema, obtener_subsistemas, borrar_subsistema

def limpiar_tabla_subsistemas(conexion):
    """
    Función para limpiar la tabla Subsistemas en una base de datos dada.
    """
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Subsistemas')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="Subsistemas"')
    conexion.commit()

class TestSubsistemas(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para cada test.
        Limpia la tabla Subsistemas antes de comenzar.
        """
        # Conectarse a la base de datos real
        self.conexion = sqlite3.connect('BD_Requisitos.db')
        limpiar_tabla_subsistemas(self.conexion)

    def tearDown(self):
        """
        Limpieza posterior a cada test.
        Limpia la tabla Subsistemas y cierra la conexión a la base de datos.
        """
        limpiar_tabla_subsistemas(self.conexion)
        self.conexion.close()

    def test_insertar_subsistema(self):
        """
        Prueba que inserta subsistemas y verifica que fueron insertados correctamente.
        """
        # Insertar subsistemas
        insertar_subsistema("Energía")
        insertar_subsistema("Comunicaciones")

        # Obtener subsistemas de la base de datos
        subsistemas = obtener_subsistemas()

        # Verificar que los subsistemas insertados están presentes
        nombres_esperados = ["Energía", "Comunicaciones"]
        nombres_obtenidos = [subsistema[1] for subsistema in subsistemas]
        self.assertEqual(set(nombres_obtenidos), set(nombres_esperados))

    def test_borrar_subsistema(self):
        """
        Prueba que inserta y luego borra un subsistema, verificando que fue eliminado correctamente.
        """
        # Insertar subsistemas
        insertar_subsistema("Energía")
        insertar_subsistema("Comunicaciones")

        # Obtener subsistemas
        subsistemas = obtener_subsistemas()
        self.assertEqual(len(subsistemas), 2)

        # Buscar el ID del primer subsistema e intentar eliminarlo
        subsistema_id = subsistemas[0][0]

        # Borrar el primer subsistema usando su ID
        borrar_subsistema(subsistema_id)

        # Verificar que el subsistema ha sido eliminado
        subsistemas_actualizados = obtener_subsistemas()
        nombres_obtenidos = [subsistema[1] for subsistema in subsistemas_actualizados]
        self.assertNotIn("Energía", nombres_obtenidos)

if __name__ == "__main__":
    unittest.main()
