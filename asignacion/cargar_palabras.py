import csv

# Función para leer el archivo CSV con ';' como delimitador
def cargar_palabras_desde_csv(ruta_csv):
    subsistemas_palabras = {}

    # Abrir el archivo CSV con el delimitador ";"
    with open(ruta_csv, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=';')  # Usar ';' como delimitador

        for fila in lector_csv:
            # Ignorar filas vacías o incompletas
            if len(fila) < 2 or not fila[1].strip():
                print(f"Fila incompleta o sin palabras clave ignorada: {fila}")
                continue

            subsistema = fila[0].strip()  # Primera columna: subsistema
            palabras_clave = fila[1:]  # Desde la segunda columna en adelante: palabras clave

            # Guardar las palabras clave en el diccionario
            subsistemas_palabras[subsistema] = [palabra.strip() for palabra in palabras_clave if palabra.strip()]

    return subsistemas_palabras

# Verificación de la lectura del CSV
if __name__ == "__main__":
    subsistemas = cargar_palabras_desde_csv("TOKENES.csv")
    
    # Imprimir los subsistemas y sus palabras clave para verificar que se han leído correctamente
    for subsistema, palabras in subsistemas.items():
        print(f"{subsistema}: {palabras}")
