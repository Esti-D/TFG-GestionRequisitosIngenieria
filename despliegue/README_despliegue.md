# Guía de despliegue del ejecutable

Esta guía explica cómo generar y ejecutar el ejecutable del proyecto utilizando los scripts incluidos en la carpeta `despliegue`.

## Requisitos previos

1. **Python**:
   - Asegúrate de tener Python 3.7 o superior instalado en tu sistema.
   - Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

2. **Instalar PyInstaller**:
   - Abre una terminal o consola y ejecuta:
     ```bash
     pip install pyinstaller
     ```

## Estructura del proyecto

Asegúrate de que tu proyecto esté organizado de la siguiente manera:

```
/mi_proyecto
├── /src
│   ├── main.py
│   └── otros_archivos.py
├── /resources
│   ├── BD_Requisitos.db
│   ├── /logos
│   ├── /idiomas
│   ├── /interfaz
│   └── /asignacion
├── /despliegue
│   ├── build.bat       # Script para Windows
│   ├── build.sh        # Script para Linux/Mac
│   └── README.md       # Este archivo
├── README.md
└── requirements.txt
```

## Generar el ejecutable

### En Windows

1. Abre el archivo `build.bat` desde la carpeta `despliegue`. 
   - Puedes hacer doble clic o ejecutarlo desde la terminal:
     ```cmd
     despliegue\build.bat
     ```
2. El script generará el ejecutable en la carpeta `dist/` como `main.exe`.

### En Linux/Mac

1. Abre una terminal y navega al directorio del proyecto.
2. Da permisos de ejecución al script:
   ```bash
   chmod +x despliegue/build.sh
   ```
3. Ejecuta el script:
   ```bash
   ./despliegue/build.sh
   ```
4. El ejecutable se generará en la carpeta `dist/` como `main`.

## Ejecutar el programa

1. Copia los siguientes archivos y carpetas en el mismo directorio que el ejecutable generado:
   - `BD_Requisitos.db`
   - Carpeta `logos/`
   - Carpeta `idiomas/`
   - Carpeta `interfaz/`
   - Carpeta `asignacion/`

2. Ejecuta el programa:
   - En **Windows**: Haz doble clic en `main.exe`.
   - En **Linux/Mac**: Abre la terminal, navega al directorio y ejecuta:
     ```bash
     ./main
     ```

## Solución de problemas

### Error al cargar la base de datos
- Asegúrate de que `BD_Requisitos.db` esté en el mismo directorio que el ejecutable.

### Archivos faltantes
- Confirma que las carpetas y archivos necesarios están completos y en las rutas indicadas.

## Detalles de los scripts

### build.bat (Windows)
```cmd
@echo off
echo Generando ejecutable con PyInstaller...

REM Cambiar al directorio raíz del proyecto
cd ..

REM Ejecutar PyInstaller
pyinstaller --noconfirm --onefile --console ^
--add-data "resources\BD_Requisitos.db;." ^
--add-data "resources\logos;logos/" ^
--add-data "resources\idiomas;idiomas/" ^
--add-data "resources\interfaz\d_bloque_otros\ayuda\help_castellano.md;interfaz/d_bloque_otros/ayuda/" ^
--add-data "resources\interfaz\d_bloque_otros\ayuda\help_ingles.md;interfaz/d_bloque_otros/ayuda/" ^
--add-data "resources\interfaz\d_bloque_otros\ayuda\help_frances.md;interfaz/d_bloque_otros/ayuda/" ^
--add-data "resources\interfaz\d_bloque_otros\ayuda\help_euskera.md;interfaz/d_bloque_otros/ayuda/" ^
--add-data "resources\asignacion\tokenes.csv;asignacion/" ^
src\main.py

REM Mensaje final
echo Ejecutable generado en dist\main.exe
pause
```

### build.sh (Linux/Mac)
```bash
#!/bin/bash
echo "Generando ejecutable con PyInstaller..."

# Cambiar al directorio raíz del proyecto
cd ..

# Ejecutar PyInstaller
pyinstaller --noconfirm --onefile --console \
--add-data "resources/BD_Requisitos.db:." \
--add-data "resources/logos:logos/" \
--add-data "resources/idiomas:idiomas/" \
--add-data "resources/interfaz/d_bloque_otros/ayuda/help_castellano.md:interfaz/d_bloque_otros/ayuda/" \
--add-data "resources/interfaz/d_bloque_otros/ayuda/help_ingles.md:interfaz/d_bloque_otros/ayuda/" \
--add-data "resources/interfaz/d_bloque_otros/ayuda/help_frances.md:interfaz/d_bloque_otros/ayuda/" \
--add-data "resources/interfaz/d_bloque_otros/ayuda/help_euskera.md:interfaz/d_bloque_otros/ayuda/" \
--add-data "resources/asignacion/tokenes.csv:asignacion/" \
src/main.py

echo "Ejecutable generado en dist/main"
```
