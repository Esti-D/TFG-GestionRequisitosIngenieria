import os
from almacenamiento.db import crear_tablas
from interfaz.interfaz_principal import iniciar_interfaz

def iniciar_aplicacion():
    # Verificar si la base de datos ya existe
    if not os.path.exists('BD_Requisitos.db'):
        print("La base de datos no existe, creando tablas...")
        crear_tablas()

    # Iniciar la interfaz gráfica
    iniciar_interfaz()

if __name__ == "__main__":
    iniciar_aplicacion()
