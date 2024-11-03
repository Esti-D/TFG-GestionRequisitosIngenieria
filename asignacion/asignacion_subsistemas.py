import csv
import ast
import os

from .cargar_palabras import cargar_palabras_desde_csv
from .trie import Trie


# Función para construir un Trie para cada subsistema
def construir_trie_para_subsistemas(subsistemas_palabras):
    """
    Construye un Trie para cada subsistema a partir de las palabras clave.
    """
    subsistemas_trie = {}

    # Iterar sobre cada subsistema y sus palabras clave
    for subsistema, palabras_clave in subsistemas_palabras.items():
        trie = Trie()  # Crear un Trie para el subsistema
        for palabra in palabras_clave:
            trie.insertar_palabra(
                palabra.lower()
            )  # Insertar cada palabra clave en el Trie
        subsistemas_trie[subsistema] = trie  # Asociar el Trie con el subsistema

    return subsistemas_trie


# Función para asignar subsistemas a un documento basado en el contenido y los Tries
def asignar_subsistemas_a_documento_trie(texto_documento, subsistemas_trie):
    """
    Asigna subsistemas a un documento según las palabras clave encontradas en el documento.
    Si se encuentran 3 o más palabras clave de un subsistema, se sugiere ese subsistema.
    """
    subsistemas_sugeridos = {}

    # Dividir el texto del documento en palabras (simplemente por espacios)
    palabras_documento = texto_documento.lower().split()

    # Recorrer cada subsistema y su Trie
    for subsistema, trie in subsistemas_trie.items():
        contador_coincidencias = 0

        # Buscar cada palabra del documento en el Trie del subsistema
        for palabra in palabras_documento:
            if trie.buscar_palabra(palabra):
                contador_coincidencias += 1

        # Si hay al menos 3 coincidencias, sugerimos el subsistema
        if contador_coincidencias >= 3:
            subsistemas_sugeridos[subsistema] = contador_coincidencias

    return subsistemas_sugeridos


# Función para asignar subsistemas a un documento (para ser llamada desde bloque_load.py)
def asignar_subsistemas_a_documento(texto_documento):
    # Obtener la ruta de la carpeta actual donde se encuentra el script
    ruta_base = os.path.dirname(
        os.path.abspath(__file__)
    )  # Ruta base del archivo actual

    # Combinar la ruta base con la carpeta  asignacion  y el archivo  TOKENES.csv
    ruta_csv = os.path.join(ruta_base, "TOKENES.csv")

    # Cargar las palabras clave desde el archivo CSV
    subsistemas_palabras = cargar_palabras_desde_csv(ruta_csv)

    # Construir los Tries para cada subsistema
    subsistemas_trie = construir_trie_para_subsistemas(subsistemas_palabras)

    # Asignar subsistemas basados en el texto del documento
    subsistemas_sugeridos = asignar_subsistemas_a_documento_trie(
        texto_documento, subsistemas_trie
    )

    return subsistemas_sugeridos
