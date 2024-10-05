import sqlite3

def listar_tablas():
    conexion = sqlite3.connect('BD_Requisitos.db')
    cursor = conexion.cursor()

    # Consultar las tablas existentes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()

    conexion.close()
    return tablas

if __name__ == "__main__":
    tablas = listar_tablas()
    print("Tablas en la base de datos:")
    for tabla in tablas:
        print(tabla[0])
