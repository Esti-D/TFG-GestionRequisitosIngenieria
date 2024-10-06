import unittest
import sqlite3
from almacenamiento.func_relaciones import (
    insertar_relacion_documento_subsistema,
    obtener_subsistemas_por_documento,
    obtener_documentos_por_subsistema,
    borrar_relacion_documento_subsistema
)

def limpiar_tabla_relaciones(conexion):
    """
    Función para limpiar la tabla Asociacion_Documento_Subsistema en una base de datos dada.
    """
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Asociacion_Documento_Subsistema')
    conexion.commit()

class TestRelaciones(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para cada test.
        Limpia la tabla de relaciones antes de comenzar.
        """
        # Conectarse a la base de datos real
        self.conexion = sqlite3.connect('BD_Requisitos.db')
        limpiar_tabla_relaciones(self.conexion)

    def tearDown(self):
        """
        Limpieza posterior a cada test.
        Limpia la tabla de relaciones y cierra la conexión a la base de datos.
        """
        limpiar_tabla_relaciones(self.conexion)
        self.conexion.close()

    def test_insertar_relacion(self):
        """
        Prueba que inserta relaciones entre documentos y subsistemas y verifica que se guardan correctamente.
        """
        # Insertar relaciones (suponiendo que el documento con ID 1 y los subsistemas con IDs 1 y 2 existen)
        insertar_relacion_documento_subsistema(1, 1)
        insertar_relacion_documento_subsistema(1, 2)

        # Consultar subsistemas asociados al documento con ID 1
        subsistemas = obtener_subsistemas_por_documento(1)

        # Verificar que los subsistemas 1 y 2 están asociados al documento 1
        subsistemas_esperados = [1, 2]
        subsistemas_obtenidos = [subsistema[0] for subsistema in subsistemas]
        self.assertEqual(set(subsistemas_obtenidos), set(subsistemas_esperados))

    def test_borrar_relacion(self):
        """
        Prueba que inserta y luego borra una relación entre un documento y un subsistema.
        Verifica que la relación fue eliminada correctamente.
        """
        # Insertar relaciones
        insertar_relacion_documento_subsistema(1, 1)
        insertar_relacion_documento_subsistema(1, 2)

        # Borrar la relación entre el documento 1 y el subsistema 1
        borrar_relacion_documento_subsistema(1, 1)

        # Consultar subsistemas asociados al documento con ID 1 después del borrado
        subsistemas_actualizados = obtener_subsistemas_por_documento(1)
        subsistemas_obtenidos = [subsistema[0] for subsistema in subsistemas_actualizados]

        # Verificar que el subsistema 1 ha sido eliminado de las relaciones
        self.assertNotIn(1, subsistemas_obtenidos)

if __name__ == "__main__":
    unittest.main()
