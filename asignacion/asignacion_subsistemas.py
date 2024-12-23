"""
Archivo: asignacion_subsistemas.py
Descripción: Funciones para asignar subsistemas a un documento en función de palabras clave mediante estructuras Trie.
Autor: Estíbalitz Díez
Fecha: 23/12/2024
Versión: 2
"""

import os

from .cargar_palabras import cargar_palabras_desde_csv
from .trie import Trie

def construir_trie_para_subsistemas(subsistemas_palabras):
    """
    Construye un Trie para cada subsistema a partir de las palabras clave.

    Args:
        subsistemas_palabras (dict): Diccionario con los subsistemas como claves y listas de palabras clave como valores.

    Returns:
        dict: Diccionario donde las claves son los subsistemas y los valores son objetos Trie construidos con las palabras clave.
    """
    subsistemas_trie = {}

    for subsistema, palabras_clave in subsistemas_palabras.items():
        trie = Trie()
        for palabra in palabras_clave:
            trie.insertar_palabra(palabra.lower())  # Insertar palabra clave en el Trie
        subsistemas_trie[subsistema] = trie

    return subsistemas_trie

def asignar_subsistemas_a_documento_trie(texto_documento, subsistemas_trie):
    """
    Asigna subsistemas a un documento según las palabras clave encontradas en el texto.

    Si se encuentran 3 o más palabras clave de un subsistema, se sugiere ese subsistema.

    Args:
        texto_documento (str): Texto completo del documento.
        subsistemas_trie (dict): Diccionario con subsistemas y sus respectivos objetos Trie.

    Returns:
        dict: Diccionario con los subsistemas sugeridos y el conteo de palabras clave encontradas.
    """
    subsistemas_sugeridos = {}
    palabras_documento = texto_documento.lower().split()  # Dividir texto en palabras

    for subsistema, trie in subsistemas_trie.items():
        contador_coincidencias = sum(1 for palabra in palabras_documento if trie.buscar_palabra(palabra))

        if contador_coincidencias >= 3:  # Sugerir subsistema si hay al menos 3 coincidencias
            subsistemas_sugeridos[subsistema] = contador_coincidencias

    return subsistemas_sugeridos

def asignar_subsistemas_a_documento(texto_documento):
    """
    Asigna subsistemas a un documento utilizando palabras clave almacenadas en un archivo CSV.

    Args:
        texto_documento (str): Texto completo del documento.

    Returns:
        dict: Diccionario con los subsistemas sugeridos y el conteo de palabras clave encontradas.
    """
    ruta_base = os.path.dirname(os.path.abspath(__file__))  # Ruta base del archivo actual
    ruta_csv = os.path.join(ruta_base, "TOKENES.csv")  # Ruta al archivo TOKENES.csv

    subsistemas_palabras = cargar_palabras_desde_csv(ruta_csv)  # Cargar palabras clave
    subsistemas_trie = construir_trie_para_subsistemas(subsistemas_palabras)  # Construir Tries
    subsistemas_sugeridos = asignar_subsistemas_a_documento_trie(
        texto_documento, subsistemas_trie
    )

    return subsistemas_sugeridos
