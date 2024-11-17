import csv
import ast


# Función para leer el archivo CSV con ';' como delimitador y procesar la columna 'tokenes'
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

    # Abrir el archivo CSV con el delimitador ";" y codificación UTF-8
    with open(ruta_csv, newline="", encoding="utf-8") as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=";")

        # Omitir el encabezado si existe
        next(lector_csv, None)

        for fila in lector_csv:
            # Ignorar filas vacías o incompletas
            if len(fila) < 2 or not fila[1].strip():
                print(f"Fila incompleta o sin palabras clave ignorada: {fila}")
                continue

            # Primera columna: Nombre del subsistema
            subsistema = fila[0].strip()

            # Segunda columna: Lista de palabras clave en formato de cadena
            tokenes_str = fila[1].strip()

            # Convertir la cadena de lista a una lista real usando ast.literal_eval
            try:
                palabras_clave = ast.literal_eval(tokenes_str)
            except (ValueError, SyntaxError):
                print(
                    f"Error al convertir la lista de palabras clave para el subsistema {subsistema}: {tokenes_str}"
                )
                continue

            # Guardar las palabras clave en el diccionario
            subsistemas_palabras[subsistema] = palabras_clave

    return subsistemas_palabras


# Verificación de la lectura del CSV
if __name__ == "__main__":
    """
    Código de prueba para verificar la funcionalidad de la lectura del archivo CSV.
    Carga los subsistemas y sus palabras clave desde un archivo llamado "TOKENES.csv"
    y los imprime en consola.
    """
    subsistemas = cargar_palabras_desde_csv("TOKENES.csv")

    # Imprimir los subsistemas y sus palabras clave para verificar que se han leído correctamente
    for subsistema, palabras in subsistemas.items():
        print(f"{subsistema}: {palabras}")
