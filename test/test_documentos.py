import unittest
import sqlite3
from almacenamiento.func_documentos import insertar_documento, obtener_documentos, borrar_documento

def limpiar_tabla_documentos(conexion):
    """
    Función para limpiar la tabla Documentos en una base de datos dada.
    """
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Documentos')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="Documentos"')
    conexion.commit()

class TestDocumentos(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para cada test.
        Limpia la tabla Documentos antes de comenzar.
        """
        # Conectarse a la base de datos real
        self.conexion = sqlite3.connect('BD_Requisitos.db')
        limpiar_tabla_documentos(self.conexion)

    def tearDown(self):
        """
        Limpieza posterior a cada test.
        Limpia la tabla Documentos y cierra la conexión a la base de datos.
        """
        limpiar_tabla_documentos(self.conexion)
        self.conexion.close()

    def test_insertar_documento(self):
        """
        Prueba que inserta varios documentos y verifica que fueron insertados correctamente.
        """
        # Insertar documentos (suponiendo que las ciudades con ID 1 y 2 existen)
        insertar_documento("Plan de Ingeniería", "1.0", 1)  # Documento vinculado a Ciudad 1
        insertar_documento("Especificaciones Técnicas", "1.2", 2)  # Documento vinculado a Ciudad 2

        # Obtener documentos de la base de datos
        documentos = obtener_documentos()

        # Verificar que los documentos insertados están presentes
        titulos_esperados = ["Plan de Ingeniería", "Especificaciones Técnicas"]
        titulos_obtenidos = [documento[1] for documento in documentos]
        self.assertEqual(set(titulos_obtenidos), set(titulos_esperados))

    def test_borrar_documento(self):
        """
        Prueba que inserta y luego borra un documento, verificando que fue eliminado correctamente.
        """
        # Insertar documentos
        insertar_documento("Plan de Ingeniería", "1.0", 1)
        insertar_documento("Especificaciones Técnicas", "1.2", 2)

        # Obtener documentos
        documentos = obtener_documentos()
        self.assertEqual(len(documentos), 2)

        # Buscar el ID del primer documento e intentar eliminarlo
        documento_id = documentos[0][0]

        # Borrar el primer documento usando su ID
        borrar_documento(documento_id)

        # Verificar que el documento ha sido eliminado
        documentos_actualizados = obtener_documentos()
        titulos_obtenidos = [documento[1] for documento in documentos_actualizados]
        self.assertNotIn("Plan de Ingeniería", titulos_obtenidos)

if __name__ == "__main__":
    unittest.main()
