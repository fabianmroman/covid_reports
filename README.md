Reportes de Covid-19 - versi�n 1 

Este proyecto genera reportes en planillas de Excel de provincias de Argentina y de pa�ses del mundo a partir de informaci�n disponible p�blicamente.
Para el caso de Argentina, el dataset se genera a partir de PDFs y contiene los casos diarios y acumulados por cada provincia (./csv/provincias.csv). 
En las planillas se incorporan indicadores que facilitan el an�lisis y entendimiento de los datos.


C�mo comenzo esto

A fines de marzo 2020, cuando supe que estaban disponibles los datasets con informacion a nivel mundial (https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases), quise poder generar mis propios reportes de determinados pa�ses. 
Como mi conocimiento de Python era muy b�sico, comenc� a hacerlo en Excel, con todas sus limitaciones y procedimientos manuales. 
En julio retom� por unos d�as mi aprendizaje de Python y luego comenc� a poner manos a la obra en este primer proyecto en Python, us�ndolo con prop�sitos de aprendizaje. 


�Por qu� analizo los datos del COVID-19?

Porque son datos que se actualizan diariamente, que simulan perfectamente la vida real respecto a datos cargados a mano, a datos faltantes, datos que se actualizan el d�a siguiente, etc, para generar datos limpios.  


�Qu� hay de distinto? 

Se calcula el tiempo de duplicaci�n (m�todo sim�trico), indicador que no vi en ning�n desarrollo hasta el momento. 


�Por qu� saqu� los datos a partir de un PDF? 

Porque reci�n en mayo se comenzaron a publicar los datos en forma de dataset, abiertamente. A fines de julio (por medio de Sistemas Mapache) me enter� de la existencia de esos datos. 
Adem�s, me pareci� buena pr�ctica para aprender c�mo sacar datos de una fuente que no fue preparada para ser analizada. 


Detalles a tener en cuenta 

Durante el mes de marzo los reportes se emitieron de forma desorganizada, por lo tanto carecen de formato para poder ser procesados por un script. Por esta raz�n el mes de marzo fue cargado manualmente casi en su totalidad. El script utilizado y el dataset generado est� en la carpeta ./pdf/marzo. 



Contenido: 

Carpetas
- csv: contiene los datasets que se utilizan para analizar informaci�n de provincias. provincias.csv es el dataset actualizado y provincias_marzo.csv es el dataset de marzo creado casi manualmente. 
- pdf: se guardan los PDF que se bajan para ser analizados e incorporados al dataset provincias.csv por el script sortfilenames.py
- xlsx: all� se guardan los archivos que generan los scripts.
- versioning: versiones antiguas de los scripts.
- tests: pruebas realizadas para armar los scripts. 

Scripts
- sortfilenames.py: Actualiza el dataset ./csv/provincias.csv
- duplicate.py: Genera una planilla Excel por cada pa�s seleccionado usando como base los datasets globales de humdata.org.
- duplicate-prov.py: Genera una planilla Excel por cada provincia argentina seleccionada usando como base el dataset generado por el script sortfilenames.py. 



Uso
- Clonar el repositorio localmente. 
- Para datos de provincias ejecutar previamente ./sortfilenames.py para actualizar el dataset. Luego ./duplicate-prov.py. La l�nea de comandos pedir� las provincias de las cuales se quiere obtener una planilla.
- Para datos de pa�ses ejecutar ./duplicate.py. La l�nea de comandos pedir� los pa�ses (en ingl�s) de los cuales se quiere obtener una planilla.


Issues
- Como los datos se cargan a mano, pueden haber variaciones con los nombres de archivo no consideradas. Puede ocurrir tambien que cambien la forma de nombrar el directorio del mes (ocurri� en agosto). Cuando migre el an�lisis al dataset oficial no ser� necesario estar pendiente de esto. 



Pendientes - To Do 

- Desarrollar el script a partir del dataset publicado por el Ministerio de Salud.
- Agregar gr�ficos. 
- Llevar los reportes a un sitio web interactivo. 
- Mejorar funci�n que calcula el tiempo de duplicaci�n.
- Estructura modularizada para poder obtener las variables y funciones de un �nico lugar. 
- Agregar datos de localidades.
