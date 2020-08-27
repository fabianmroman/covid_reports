from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import re
import pandas as pd
import os
from urllib.request import *

opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
install_opener(opener)

url = "https://www.argentina.gob.ar/sites/default/files/02-07-20-reporte-vespertino-covid-19.pdf"
pdf_file = url.split('/')[-1]
urlretrieve (url, pdf_file)
fp = open(pdf_file, 'rb')

rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = PDFPage.get_pages(fp)

fecha = re.split('_|-',pdf_file)
if len(fecha[0]) == 1:
    fecha[0] = "0" + fecha[0]
fecha = fecha[0] + "/" + fecha[1] + "/" + fecha[2]

row_list=[]

for page in pages:
    interpreter.process_page(page)
    layout = device.get_result()
    for lobj in layout:
        if isinstance(lobj, LTTextBox):
            paragraph = lobj.get_text()
            paragraph = paragraph.split("\n")
            #print (paragraph)
            for line in paragraph:
                if "|" in line:   # Sacar datos de provincias nada mas
                    if line[0:7] != "Detalle":
                        line = line[3:]
                        line = line.replace(".","")
                        line = line[::-1] # Poner string al reves para separar datos
                        if line[0:1] != "":
                            line = line[1::]
                            print (line)
                            line = line.split(" | ")
                            total = line[0][::-1] # Asignar y dar vuelta el nro
                            line1 = line[1].split(" ")
                            diario = line1[0][::-1]
                            provincia=""
                            for provincia_r in line1[1:]:
                                if provincia_r == "**ogeuF":
                                    provincia_r = "ogeuF"
                                provincia = provincia + " " + provincia_r
                            print (provincia)
                            provincia = provincia[::-1]
                            print (provincia)
                            provincia = provincia[0:len(provincia)-1] 
                            if provincia[-1] == " ": # Segundo espacio en Chubut
                                provincia = provincia[0:len(provincia)-1]
                            print (provincia)
                            datos = [fecha, provincia, diario, total]
                            row_list.append(datos)
                        


csv_file = "provincias.csv"

df = pd.DataFrame (row_list, columns = ['Fecha','Provincia','Diario','Acumulado'])
df = df.set_index('Fecha')

# df.append(df2, ignore_index=True)

print (row_list)
print (df)
                            
hdr = False if os.path.isfile(csv_file) else True
df.to_csv(csv_file, mode='a', header=hdr, encoding="utf-16")

