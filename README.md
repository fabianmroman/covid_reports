Reportes de Covid-19 - versión 1 

Este proyecto genera reportes en planillas de Excel de provincias de Argentina y de países del mundo a partir de información disponible públicamente. Para el caso de Argentina, el dataset se genera a partir de PDFs. En las planillas se incorporan indicadores que facilitan el análisis y entendimiento de los datos.


Cómo comenzo esto

A fines de marzo 2020, cuando supe que estaban disponibles los datasets con informacion a nivel mundial (https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases), quise poder generar mis propios reportes de determinados países. 
Como mi conocimiendo de Python era muy básico, comencé a hacerlo en Excel, con todas sus limitaciones y procedimientos manuales. 
En julio retomé por unos días mi aprendizaje de Python y luego comencé a poner manos a la obra en este primer proyecto en Python, usándolo con propósitos de aprendizaje. 


¿Por qué analizo los datos del COVID-19?

Porque son datos que se actualizan diariamente, que simulan perfectamente la vida real respecto a datos  datos cargados a mano, a datos faltantes, datos que se actualizan el día siguiente, etc, para generar datos limpios.  


¿Qué hay de distinto? 

Se calcula el tiempo de duplicación (método simétrico), indicador que no vi en ningún desarrollo hasta el momento. 


¿Por qué saqué los datos a partir de un PDF? 

Porque recién en mayo se comenzaron a publicar los datos en forma de dataset, abiertamente. Recién a fines de julio (por medio de Sistemas Mapache) me enteré de la existencia de esos datos. 
Además, me pareció buena práctica para aprender cómo sacar datos de una fuente que no fue preparada para ser analizada. 


Detalles a tener en cuenta 

Durante el mes de marzo los reportes se emitieron de forma desorganizada, por lo tanto carecen de formato para poder ser procesados por un script. Por esta razón el mes de marzo fue cargado manualmente casi en su totalidad. El script utilizado y el dataset generado está en la carpeta ./pdf/marzo. 



Contenido: 

Carpetas
- csv: contiene los datasets que se utilizan para analizar información de provincias. provincias.csv es el dataset actualizado y provincias_marzo.csv es el dataset de marzo creado casi manualmente. 
- pdf: se guardan los PDF que se bajan para ser analizados e incorporados al dataset provincias.csv por el script sortfilenames.py
- xlsx: allí se guardan los archivos que generan los scripts.
- versioning: versiones antiguas de los scripts.
- tests: pruebas realizadas para armar los scripts. 

Scripts
- sortfilenames.py: Actualiza el dataset ./csv/provincias.csv
- duplicate.py: Genera una planilla Excel por cada país seleccionado usando como base los datasets globales de humdata.org.
- duplicate-prov.py: Genera una planilla Excel por cada provincia argentina seleccionada usando como base el dataset generado por el script sortfilenames.py. 



Uso
- Clonar el repositorio localmente. 
- Para datos de provincias ejecutar previamente ./sortfilenames.py para actualizar el dataset. Luego ./duplicate-prov.py. La línea de comandos pedirá las provincias de las cuales se quiere obtener una planilla.
- Para datos de países ejecutar ./duplicate.py. La línea de comandos pedirá los países (en inglés) de los cuales se quiere obtener una planilla.


Issues
- Como los datos se cargan a mano, pueden haber variaciones con los nombres de archivo no consideradas. Puede ocurrir tambien que cambien la forma de nombrar el directorio del mes (ocurrió en agosto). Cuando migre el análisis al dataset oficial no será necesario estar pendiente de esto. 
- Solucionar el warning SettingWithCopyWarning. 



Pendientes - To Do 

- Desarrollar el script a partir del dataset publicado por el Ministerio de Salud.
- Agregar gráficos. 
- Llevar los reportes a un sitio web interactivo. 
- Mejorar función que calcula el tiempo de duplicación.
- Comenzar a trabajar desde Github, para manetener versionado. Hasta no tener una versión limpia no quería subirlo. De todas maneras las sucesivas versiones y mejoras hasta llegar al código actual están en la carpeta "versioning". 
- Estructura modularizada para poder obtener las variables y funciones de un único lugar. 
- Selección sin usar acentos. 
- Agregar datos de localidades.
- Chequear existencia de estructura de directorios.
