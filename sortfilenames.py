"""
Este script actualiza el dataset ./csv/provincias.csv a partir de los PDF disponibles diariamente
por el Ministerio de Salud. Luego pueden separarse los datos por provincias con el script
duplicate-prov.py.


    CHANGELOG
    
    Version final v1.1 10/07/2020 para obtener todos los archivos antiguos
    con todas las correciones hechas y crear el dataset, funcionando
    perfectamente. Podria hasta obtener los archivos con solo descomentar
    la linea urlretrieve

    v1.2 16/07/2020 usando el urlretrieve para el mes actual. Antes hay que borrar en el
    csv las lineas correspondientes al mes que se va a bajar, porque no se esta
    haciendo ese chequeo
    Corregido la obtencion de archivos dependiendo de lo que haya (vesp, mat)

    v1.3 20/07/2020
    Chequea el dataset para ver la última fecha disponible y bajar los ultimos datos
    Si no hay datos crea el dataset completo a partir del 1/04/2020. Los datos de marzo
    quedan en un dataset fijo que se toma como base ya que son dificiles de obtener
    automaticamente desde los pdfs pues no habia un estandar en el formato del informe.
    22/07/2020
    Hecho, falta el chequeo de archivos existentes antes de ejecutar
    Corregida la captura de fechas si el primer archivo es un matutino, no se pierden al cortar
    la lista, se mantiene y se decrementa el maxdate para saber que es del dia anterior
    Si los archivos ya existen, no se vuelven a bajar.
    Se corrigio el dataset base de marzo, que tenia el año en formato largo.

    v1.4 23/07/2020
    Se chequea de que se dispongan los archivos antes de comenzar. De lo contrario, baja desde
    Github el base y construye los datos desde abril. Tambien podria bajar el archivo mas
    actualizado.
    Mejorada la logica para eliminar matutinos con informacion repetida.
    Los PDF se guardan en otro path para mantener el orden. El dataset se genera
    en la misma ubicacion de los archivos de reportes (antes estaba junto con los
    PDF).
    3/08/2020
    Modificada URL porque pusieron "agosto-de-2020", rompiendo el estandar anterior :angry:
    5/08/2020
    Corregidos detalles a la hora de cargar los informes nuevos. 
    
    v1.5 10/08/2020 Final
    Ultima version que extrae datos a partir de los PDF. A partir de ahora es mas efectivo extraer
    los datos del dataset original, disponible en: 
    https://docs.google.com/spreadsheets/d/16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA/export?format=csv&id=16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA&gid=0
    Link publicado en https://github.com/SistemasMapache/Covid19arData
    12/08/2020
    Paths separados para cada tipo de archivo

    v1.5.1
    Corregido error al actualizar el dataset para el dia actual, no decrementa maxdate del matutino si ya hay
    un vespertino de ese dia.
    Verificado para mes septiembre. Corregida URL de base. 
"""

from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import pandas as pd
from urllib.request import * #Request, urlopen, urlretrieve
from datetime import date
from calendar import monthrange
import re
import os
import sys

CSV_FILE = "./csv/provincias.csv"
CSV_PROVINCIAS_MARZO = "./csv/provincias_marzo.csv"
PATHPDF = "./pdf/"

# Preparar el downloader con los headers
opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
install_opener(opener)

# Carga / creacion del dataset desde un archivo csv. El archivo csv inicial (mes de marzo) es provincias_marzo.csv

# Chequear existencia del archivo csv con el dataset
provFile = False
provmarzoFile = False

try:
    with open(CSV_FILE, 'r') as f:
        if len(f.read()) >= 31750:  # Dataset con datos mas alla de marzo
            provFile = True
        else:
            f.close()
            urlretrieve("https://raw.githubusercontent.com/fabianmroman/covid_reports_v1/master/csv/provincias.csv", CSV_FILE)
            with open(CSV_FILE, 'r') as f:
                if len(f.read()) >= 31750: # Dataset de marzo bajado correctamente
                    provFile = True
        f.close()
except:  # archivo inexistente
    urlretrieve("https://raw.githubusercontent.com/fabianmroman/covid_reports_v1/master/csv/provincias.csv", CSV_FILE)
    with open(CSV_FILE, 'r') as f:
        if len(f.read()) >= 31750: # Dataset de marzo bajado correctamente
            provFile = True
        f.close()

try:
    with open(CSV_PROVINCIAS_MARZO, 'r') as g:
        if len(g.read()) == 31750: # Dataset de marzo no modificado 
            provmarzoFile = True
        else:  # archivo modificado
            g.close()
            urlretrieve("https://raw.githubusercontent.com/fabianmroman/covid_reports_v1/master/csv/provincias_marzo.csv", CSV_PROVINCIAS_MARZO)
            with open(CSV_PROVINCIAS_MARZO, 'r') as g:
                if len(g.read()) == 31750: # Dataset de marzo bajado correctamente
                    provmarzoFile = True
        g.close()
except:  # archivo inexistente
    urlretrieve("https://raw.githubusercontent.com/fabianmroman/covid_reports_v1/master/csv/provincias_marzo.csv", CSV_PROVINCIAS_MARZO)
    with open(CSV_PROVINCIAS_MARZO, 'r') as g:
        if len(g.read()) == 31750: # Dataset de marzo bajado correctamente
            provmarzoFile = True
        g.close()


if not provFile and not provmarzoFile:  # En caso de modificacion de los dataset, que los copie
    if os.name == "nt":
        cmd = 'copy ' + CSV_PROVINCIAS_MARZO + ' ' + CSV_FILE
    else:
        cmd = 'cp ' + CSV_PROVINCIAS_MARZO + ' ' + CSV_FILE
    os.system (cmd)
    provFile = True



# Seccion 1a: Fechas
# ==================

# Cargar el dataset y chequear la fecha del ultimo registro disponible en el csv
if provFile:
    df = pd.read_csv(CSV_FILE, encoding="utf-16")
    last = df.tail(1)
    lasts = last.values.tolist()[0]
    fechacsv = lasts[0].split("/")  
    print (fechacsv)

    # Fecha del dia de hoy
    anio = "2020" # Esta en este formato porque es como esta en la URL
    today = date.today()
    today = today.strftime("%d-%m-%Y")
    today = today.split("-") #[dia, mes, anio]
    print (today)

    # Diccionario para hacer la traduccion mes - nro 
    meses = {"09":"septiembre", "08":"agosto", "07":"julio", "06":"junio", "05":"mayo", "04":"abril"}

    if int(fechacsv[1]) > 3: 
        count = int(today[1]) - int(fechacsv[1]) + 1
    else:
        count = int(today[1]) - int(fechacsv[1]) # csv inicial / 31-03-20
        
    print (count)
    mesesaprocesar = []

    for i in range(0,count):
        mesesaprocesar.append("0" + str (int(today[1])-i) )

    print (mesesaprocesar)

    # Seccion 1: Bajar los PDF necesarios para actualizar el dataset con los datos de provincias hasta hoy
    # ====================================================================================================


    diasanteriores=[] # Se guarda en esta lista los datos del reporte matutino anterior en caso de que falte un vespertino
    # Al estar afuera del ciclo, si falla va a tomar el dia anterior aunque cambie de mes!
    listadoarchivos = []  # Lista que contiene los archivos a agregar al dataset 

    for mes in mesesaprocesar:
        print (mes)
        print (meses[mes])
        listadodelmesdecr = [] # Para guardar los archivos del mes y luego ordenarlos
        maxdate = 0 # Fecha maxima del mes
        if meses[mes] == "agosto":  # hay que ver como lo cargan para septiembre...
            req = Request('https://www.argentina.gob.ar/informes-diarios/' + meses[mes] + "-de-" + anio, headers={'User-Agent': 'Mozilla/5.0'})
        else:
            req = Request('https://www.argentina.gob.ar/coronavirus/informes-diarios/reportes/' + meses[mes] + anio, headers={'User-Agent': 'Mozilla/5.0'})
        content = urlopen(req).read()
        content = content.decode('utf-8') # convert to a string
        content = content.split("><")

        for line in content: # Filtrado del PDF
            if "pdf" in line:
                linebef = line.split("a href=\"")[1] # capturar el inicio de la URL
                URL = linebef.split("\" class=")[0]  # capturar la URL completa
                filename = URL.split("/")[-1]
                filedate = re.split('_|-',filename) # fecha en el archivo
                if int(filedate[0]) > maxdate:
                    maxdate = int(filedate[0])
                print (URL)
                if len(filedate[0]) == 1: # si el dia en el archivo viene con un solo digito
                    filename = "0" + filename
                #print (filedate[0], diasanteriores)
        
                if "VESPERTINO" in filename.upper():
                    if diasanteriores != []: # elimina matutinos con info repetida y corrige fechas
                        fechaultimomat = diasanteriores[-1][1].split("-")
                        if int(fechaultimomat[0]) == int(filedate[0])+1 or int(fechaultimomat[0]) == 1:
                            diasanteriores = diasanteriores[0:len(diasanteriores)-1]
                            if int(fechaultimomat[0]) == int(today[0]) and not "VESPERTINO" in filename.upper():
                            # Solo decrementa si hay un unico reporte para el dia, que son datos del dia anterior
                                maxdate -=1
                        if diasanteriores != []:
                            maxdate -=1    
                    if diasanteriores != []:
                        for dias in diasanteriores:
                            if not os.path.isfile(PATHPDF + dias[1]):
                                urlretrieve(dias[0], PATHPDF + dias[1])
                            listadodelmesdecr.append(dias[1])
                    if not os.path.isfile(PATHPDF + filename):
                        urlretrieve(URL, PATHPDF + filename)
                    listadodelmesdecr.append(filename)
                    diasanteriores = []
                else:
                    diasanteriores.append([URL, filename])   
                

        print (listadodelmesdecr)
        if today[1] == mes and fechacsv[1] == mes:
            count = maxdate - int(fechacsv[0]) # Cuantos dias para atras incluir
            listadodelmesdecr = listadodelmesdecr[0:count]
        else:
            if fechacsv[1] == mes:
                count = int(monthrange(int(anio), int(mes))[1]) - int(fechacsv[0])
                listadodelmesdecr = listadodelmesdecr[0:count]
        print (maxdate)
        print (fechacsv[0])
          
        print (listadodelmesdecr)

        listadoarchivos = listadoarchivos + listadodelmesdecr

    listadoarchivos = listadoarchivos[::-1]  # Para volverlos al orden cronologico


    # Seccion 2: Actualizacion del dataset hasta la fecha actual, procesando los PDF en el listado de archivos  
    # ========================================================================================================
    
    dfrow_list=[] # guardado temporal de los datos antes de incluirlos en el DataFrame

    for pdf_file in listadoarchivos:
        fp = open(PATHPDF + pdf_file, 'rb')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.get_pages(fp)

        fecha = re.split('_|-',pdf_file)
        if "matutino" in pdf_file:
            fecha[0] = str(int(fecha[0])-1)
            if len(fecha[0]) == 1:
                fecha[0] = "0" + str(fecha[0])
        fecha = fecha[0] + "/" + fecha[1] + "/" + fecha[2] 

        for page in pages:
            interpreter.process_page(page)
            layout = device.get_result()
            for lobj in layout:
                if isinstance(lobj, LTTextBox):
                    paragraph = lobj.get_text()
                    paragraph = paragraph.split("\n")
                    for line in paragraph:
                        line = line.replace(" / ", " | ")
                        if "|" in line:   # Sacar datos de provincias nada mas
                            if line[0:7] != "Detalle":
                                line = line.strip() # Eliminar espacios
                                line = line.replace(".","")
                                line = line[::-1] # Poner string al reves para separar datos
                                if line[0:1] != "":
                                    line = line.split("|")
                                    line[1] = line[1].strip()
                                    total = line[0][::-1] # Asignar y dar vuelta el nro
                                    total = total.strip()
                                    # Si los numeros traen algun caracter raro
                                    try:
                                        int(total)
                                    except:
                                        total = re.sub("[^0-9]", "", total)
                                    line1 = line[1].split(" ")
                                    diario = line1[0][::-1]
                                    # Si los numeros traen algun caracter raro
                                    try:
                                        int(diario)
                                    except:
                                        diario = re.sub("[^0-9]", "", diario)
                                    diario = diario.strip()
                                    provincia=""
                                    for provincia_r in line1[1:]:
                                        provincia = provincia + " " + provincia_r
                                    provincia = provincia[::-1]
                                    if provincia[0] == "-":
                                        provincia = provincia[1::]
                                    provincia = provincia.replace("*","")
                                    provincia = provincia.strip()
                                    datos = [fecha, provincia, diario, total]
                                    dfrow_list.append(datos)
        fp.close()


    # Seccion 3: Agregar los datos al dataset y actualizar el archivo CSV   
    # ===================================================================
                         
    df = pd.DataFrame (dfrow_list, columns = ['Fecha','Provincia','Diario','Acumulado'])
    df = df.set_index('Fecha')

    print (df)
                                
    hdr = False if os.path.isfile(CSV_FILE) else True
    df.to_csv(CSV_FILE, mode='a', header=hdr, encoding="utf-16")
    
else:
    print ("Faltan archivos o falla la conexion a Internet")
