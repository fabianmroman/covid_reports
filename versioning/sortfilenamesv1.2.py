from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import pandas as pd
#import urllib.request
from urllib.request import * #Request, urlopen, urlretrieve
from datetime import date
from calendar import monthrange
import re
import os
import sys

""" Version final v1.1 10/07/2020 para obtener todos los archivos antiguos
    con todas las correciones hechas, y crear el dataset, funcionando
    perfectamente. Podria hasta obtener los archivos con solo descomentar
    la linea urlretrieve"""

""" v1.2 16/07/2020 usando el urlretrieve para el mes actual. Antes borrar en el
    csv las lineas correspondientes al mes que se va a bajar, porque no se esta
    haciendo ese chequeo
    Corregido la obtencion de archivos dependiendo de lo que haya (vesp, mat) """

#meses = {"julio":"07", "junio":"06", "mayo":"05", "abril":"04" }
meses = {"julio":"07"}
anio = "2020"
today = date.today()
today = today.strftime("%d-%m-%Y")
today = today.split("-") #[dia, mes, anio]

print (today)


opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
install_opener(opener)

diasanteriores=[] # se guarda linea anterior en caso de que falte un vespertino
# al estar afuera del ciclo, si falla va a tomar el dia anterior aunque cambie de mes!

listadoarchivos = []  # Para poder procesar crear el dataset 

for mes in meses:
    listadodelmesdecr = [] # Para guardar los archivos del mes y luego ordenarlos
    req = Request('https://www.argentina.gob.ar/coronavirus/informe-diario/' + mes + anio, headers={'User-Agent': 'Mozilla/5.0'})
    content = urlopen(req).read()
    content = content.decode('utf-8') # convert to a string
    content = content.split("><")
    if today[1] == meses[mes]:  # ejecucion para el mes actual, el ultimo dia es el dia actual 
        day = int(today[0]) # cantidad de dias maximo a contar
    else:
        day = monthrange(int(anio), int(meses[mes]))[1] # el maximo de dias va a ser los que tenga el mes
    for line in content:
        if "pdf" in line:
            linebef = line.split("a href=\"")[1] # capturar el inicio de la URL
            URL = linebef.split("\" class=")[0]  # capturar la URL completa
            print (URL)
            filename = URL.split("/")[-1]
            filedate = re.split('_|-',filename) # fecha en el archivo
            if len(filedate[0]) == 1: # si el dia en el archivo viene con un solo digito
                filename = "0" + filename
            print (filedate[0], diasanteriores)
            if "VESPERTINO" in filename.upper():
                diasanteriores = diasanteriores[0:len(diasanteriores)-1]
                #eliminar el dia actual, que ya tengo con el vesp)
                if diasanteriores != []:
                    for dias in diasanteriores:
                        urlretrieve(dias[0], dias[1])
                        listadodelmesdecr.append(dias[1])
                urlretrieve(URL, filename)
                listadodelmesdecr.append(filename)
                diasanteriores = []
            else:
                diasanteriores.append([URL, filename])
    listadoarchivos = listadoarchivos + listadodelmesdecr
             


print (listadodelmesdecr)

listadoarchivos = listadoarchivos[::-1]


dfrow_list=[] # guardado temporal de los datos antes de incluirlos en el DataFrame
csv_file = "provincias.csv"

for pdf_file in listadoarchivos:
    fp = open(pdf_file, 'rb')
    print (pdf_file)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)

    fecha = re.split('_|-',pdf_file)
    print (fecha)
    if "matutino" in pdf_file:
        fecha[0] = str(int(fecha[0])-1)
        if len(fecha[0]) == 1:
            fecha[0] = "0" + str(fecha[0])
    fecha = fecha[0] + "/" + fecha[1] + "/" + fecha[2]
    print (fecha)

    for page in pages:
        interpreter.process_page(page)
        layout = device.get_result()
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                paragraph = lobj.get_text()
                paragraph = paragraph.split("\n")
                #print (paragraph)
                for line in paragraph:
                    line = line.replace(" / ", " | ")
                    if "|" in line:   # Sacar datos de provincias nada mas
                        if line[0:7] != "Detalle":
                            line = line.strip()
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
                        
df = pd.DataFrame (dfrow_list, columns = ['Fecha','Provincia','Diario','Acumulado'])
df = df.set_index('Fecha')

print (df)
                            
hdr = False if os.path.isfile(csv_file) else True
df.to_csv(csv_file, mode='a', header=hdr, encoding="utf-16")











