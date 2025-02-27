# Sistema de Extracción y Gestión de Requisitos
![Versión](https://img.shields.io/badge/Versión-2.0-blue)
[![codebeat badge](https://codebeat.co/badges/8a35aa0d-8f67-4aab-ab82-e56ced93946b)](https://codebeat.co/projects/github-com-esti-d-tfg-gestionrequisitosingenieria-v2)
## Descripción

Este proyecto es un sistema de escritorio diseñado para **extraer, organizar y gestionar requisitos** desde documentos PDF. 
- Automatiza la extracción de información estructurada.
- Asigna requisitos a subsistemas de ingeniería.
- Exporta resultados en formatos compatibles (CSV).

### Características principales
- **Procesamiento de documentos PDF**: Extrae capítulos y requisitos automáticamente.
- **Gestión de requisitos**: Edición, almacenamiento y consulta en una base de datos SQLite.
- **Exportación de datos**: Compatible con herramientas avanzadas como IBM DOORS.
- **Soporte multilingüe**: Idioma configurable para entornos internacionales.

---

## Instalación

Sigue estos pasos para clonar el proyecto y configurarlo en tu entorno local:

1. Clona este repositorio:
   git clone https://github.com/Esti-D/TFG-GestionRequisitosIngenieria.git

   cd TFG
2. Instala las dependencias:
    pip install -r requirements.txt
3. Ejecuta la aplicacion
    python main.py

### Uso

1. Abre la aplicación desde la terminal siguiendo las instrucciones de instalación.
2. Carga un documento PDF desde el menú principal.
3. Revisa los requisitos extraídos automáticamente.
4. Asocia los requisitos a subsistemas según palabras clave detectadas.
5. Exporta los resultados en formato CSV para usarlos en otras herramientas.

### Estructura del Proyecto

La estructura principal del proyecto es la siguiente:

TFG/

├── main.py               # Archivo principal

├── docs/                 # Documentación generada

├── almacen/              # Código fuente

├── almacenamiento/       # Código fuente

├── asignacion/           # Código fuente

├── extraccion/           # Código fuente

├── idiomas/              # Código fuente

├── interfaz/             # Código fuente

├── requirements.txt      # Dependencias

└── README.md             # Este archivo

### Licencia
Este proyecto, TFG-RM-GestionRequisitosIngenieria, está licenciado bajo una licencia Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).

### Contacto
Para consultas o sugerencias, puedes contactarme en:

Nombre: Estíbalitz Díez

Email: edr1006@alu.ubu.es
