"""
Archivo: cargar_palabras.py
Descripción: Funciones para leer y procesar un archivo CSV con información sobre subsistemas y sus palabras clave.
Autor: Estíbalitz Díez
Fecha: 23/12/2024
Versión: 2
"""

import csv
import ast

def cargar_palabras_desde_csv(ruta_csv):
    """
    Lee un archivo CSV que contiene subsistemas y sus palabras clave (tokenes).
    Los tokenes están en formato de lista dentro de una columna específica.

    Args:
        ruta_csv (str): Ruta al archivo CSV que se desea procesar.

    Returns:
        dict: Diccionario donde las claves son los subsistemas y los valores
              son listas de palabras clave asociadas.
    """
    subsistemas_palabras = {}

    with open(ruta_csv, newline="", encoding="utf-8") as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=";")

        # Omitir el encabezado si existe
        next(lector_csv, None)

        for fila in lector_csv:
            if len(fila) < 2 or not fila[1].strip():  # Ignorar filas vacías o incompletas
                print(f"Fila incompleta o sin palabras clave ignorada: {fila}")
                continue

            subsistema = fila[0].strip()  # Nombre del subsistema
            tokenes_str = fila[1].strip()  # Lista de palabras clave como cadena

            try:
                palabras_clave = ast.literal_eval(tokenes_str)  # Convertir cadena a lista
            except (ValueError, SyntaxError):
                print(
                    f"Error al convertir la lista de palabras clave para el subsistema {subsistema}: {tokenes_str}"
                )
                continue

            subsistemas_palabras[subsistema] = palabras_clave

    return subsistemas_palabras

if __name__ == "__main__":
    """
    Código de prueba para verificar la funcionalidad de la lectura del archivo CSV.
    Carga los subsistemas y sus palabras clave desde un archivo llamado "TOKENES.csv"
    y los imprime en consola.
    """
    subsistemas = cargar_palabras_desde_csv("TOKENES.csv")

    for subsistema, palabras in subsistemas.items():
        print(f"{subsistema}: {palabras}")
