import unittest
import sqlite3
from almacenamiento.func_requisitos import insertar_requisito, obtener_requisitos, borrar_requisito

def limpiar_tabla_requisitos(conexion):
    """
    Función para limpiar la tabla Requisitos en una base de datos dada.
    """
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Requisitos')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="Requisitos"')
    conexion.commit()

class TestRequisitos(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para cada test.
        Limpia la tabla Requisitos antes de comenzar.
        """
        # Conectarse a la base de datos real
        self.conexion = sqlite3.connect('BD_Requisitos.db')
        limpiar_tabla_requisitos(self.conexion)

    def tearDown(self):
        """
        Limpieza posterior a cada test.
        Limpia la tabla Requisitos y cierra la conexión a la base de datos.
        """
        limpiar_tabla_requisitos(self.conexion)
        self.conexion.close()

    def test_insertar_requisito(self):
        """
        Prueba que inserta requisitos y verifica que fueron insertados correctamente.
        """
        # Insertar requisitos (suponiendo que los documentos con IDs 1 y 2 existen)
        insertar_requisito(2, "Requisito de Seguridad", 1)  # Requisito vinculado al documento 1
        insertar_requisito(3, "Requisito de Rendimiento", 2)  # Requisito vinculado al documento 2

        # Obtener requisitos de la base de datos
        requisitos = obtener_requisitos()

        # Verificar que los requisitos insertados están presentes
        descripciones_esperadas = ["Requisito de Seguridad", "Requisito de Rendimiento"]
        descripciones_obtenidas = [requisito[1] for requisito in requisitos]
        self.assertEqual(set(descripciones_obtenidas), set(descripciones_esperadas))

    def test_borrar_requisito(self):
        """
        Prueba que inserta y luego borra un requisito, verificando que fue eliminado correctamente.
        """
        # Insertar requisitos
        insertar_requisito(2, "Requisito de Seguridad", 1)
        insertar_requisito(3, "Requisito de Rendimiento", 2)

        # Obtener requisitos
        requisitos = obtener_requisitos()
        self.assertEqual(len(requisitos), 2)

        # Buscar el ID del primer requisito e intentar eliminarlo
        requisito_id = requisitos[0][0]

        # Borrar el primer requisito usando su ID
        borrar_requisito(requisito_id)

        # Verificar que el requisito ha sido eliminado
        requisitos_actualizados = obtener_requisitos()
        descripciones_obtenidas = [requisito[1] for requisito in requisitos_actualizados]
        self.assertNotIn("Requisito de Seguridad", descripciones_obtenidas)

if __name__ == "__main__":
    unittest.main()
