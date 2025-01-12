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
