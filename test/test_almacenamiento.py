import unittest
import sqlite3
import logging

def listar_tablas(conexion):
    """
    Función para listar las tablas de la base de datos.
    Recibe una conexión a la base de datos.
    Devuelve una lista con los nombres de las tablas.
    """
    try:
        cursor = conexion.cursor()

        # Consultar las tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()

        logging.info(f"Tablas encontradas: {[tabla[0] for tabla in tablas]}")
        return tablas

    except sqlite3.Error as e:
        logging.error(f"Error al listar las tablas: {e}")
        return []

class TestAlmacenamiento(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para cada test.
        Crea una base de datos en memoria y tablas de prueba.
        """
        # Crear base de datos en memoria
        self.conexion = sqlite3.connect(":memory:")
        cursor = self.conexion.cursor()

        # Crear tablas de ejemplo
        cursor.execute("CREATE TABLE IF NOT EXISTS Ciudad (id INTEGER PRIMARY KEY, nombre TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Documento (id INTEGER PRIMARY KEY, titulo TEXT)")
        self.conexion.commit()

    def tearDown(self):
        """
        Limpieza posterior a cada test.
        Cierra la conexión a la base de datos.
        """
        self.conexion.close()

    def test_listar_tablas(self):
        """
        Prueba que verifica si las tablas creadas se listan correctamente.
        """
        tablas = listar_tablas(self.conexion)
        tablas_esperadas = [('Ciudad',), ('Documento',)]
        
        # Comprobamos que las tablas esperadas están en la base de datos
        self.assertEqual(set(tablas), set(tablas_esperadas))

if __name__ == "__main__":
    unittest.main()

