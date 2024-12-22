## Ayuda del software RM Requirements Management

### Índice
- [Carga de documentos a la Base de Datos](#carga-de-documentos-a-la-base-de-datos)
- [Consultas](#consultas)
- [Otros](#otros)
- [Ajustes](#ajustes)
- [Ayuda](#ayuda)

---

### Carga de documentos a la Base de Datos
1. Mediante el botón **Seleccionar archivo** (que abre el explorador de archivos), elige el archivo PDF con los requisitos. Este aparecerá en la ventana del visor. Luego, inicia el proceso presionando el botón **CARGAR**. 
1.1. Búsqueda de la jerarquía de capítulos, los patrones que reconoce son: 
        1.
        1
        1-
        1) 
1.2. Patronones no reconocidos
1.2.1. En caso de no reconocimiento, la opción recomendada es "Modificar" implica que se convierta el pdf a editable mediante un software externo para incorporar uno de los patrones reconocidos y realizar la gestion de documento. 
1.2.2. La otra opción disponible es Forzar.  De este modo, todo el documento se entenderá como capítulo unico y todos los requisitos estarán en el mismo nivel jerarquico. 
1.3. Patrones reconocidos o forzados. Se mostrará una ventana para seleccionar el proyecto al que deseas añadir los requisitos.

2. Una vez seleccionado el proyecto, acepta para continuar. El proceso de carga se completará, mostrando el contenido, y permitiendo la edición (si deseas corregir o eliminar algo).
3. El sistema analizará el alcance potencial de los subsistemas y propondrá los que podrían estar afectados; podrás seleccionar algunos o todos según convenga.
   
Al finalizar, los requisitos/documento estarán almacenados y vinculados al proyecto y subsistemas correspondientes.

### Consultas
1. Puedes realizar búsquedas de requisitos, documentos, proyectos y subsistemas marcando la opción deseada.
2. Si deseas listar todos los elementos, solo debes presionar el botón **Consultar**.
3. Para realizar una búsqueda específica, usa los filtros de **Documentos**, **Proyectos** y **Subsistemas**. Puedes aplicar un único filtro o combinarlos; por ejemplo, puedes seleccionar los documentos de un proyecto específico y de un único subsistema.

### Otros
1. **Proyectos**: Puedes añadir nuevos proyectos a la base de datos para asignarles documentos y requisitos. El criterio recomendado es usar el nombre de la ciudad donde se desarrollará el proyecto. También puedes eliminar proyectos.
2. **Subsistemas**: Puedes añadir nuevos subsistemas a la base de datos. Para que un subsistema se reconozca en el análisis de alcance de un documento/requisito, es necesario incluir sus palabras clave en el archivo asociado `TOKENES.csv`. También puedes eliminar subsistemas.
3. **Asignar**: Esta opción permite crear relaciones entre documentos y subsistemas tras la carga del documento. Está diseñada para casos en los que necesites asociar un documento con otro subsistema posteriormente. También permite eliminar asociaciones.

### Ajustes
1. Puedes elegir el idioma en el que deseas trabajar con esta aplicación. En esta versión, se dispone de español, inglés y francés.

### Ayuda
1. Explicación de cada una de las opciones disponibles en esta versión del software.

