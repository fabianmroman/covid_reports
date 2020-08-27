import pandas
#import urllib.request
from urllib.request import * #Request, urlopen, urlretrieve
from datetime import date
from calendar import monthrange
import re 

""" Version final 10/07/2020 para obtener todos los archivos antiguos """

meses = {"abril":"04", "mayo":"05", "junio":"06", "julio":"07"}
#meses = {"julio":"07"}
anio = "2020"
today = date.today()
today = today.strftime("%d-%m-%Y")
today = today.split("-") #[dia, mes, anio]

print (today)


opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
install_opener(opener)

datamatutino=[] # se guarda linea anterior en caso de que falte un vespertino
# al estar afuera del ciclo, si falla va a tomar el dia anterior aunque cambie de mes!

for mes in meses:
    req = Request('https://www.argentina.gob.ar/coronavirus/informe-diario/' + mes + anio, headers={'User-Agent': 'Mozilla/5.0'})
    content = urlopen(req).read()
    content = content.decode('utf-8') # convert to a string
    content = content.split("><")
    if today[1] == meses[mes]:  # ejecucion para el mes actual, el ultimo dia es el dia actual 
        day = int(today[0]) # cantidad de dias maximo a contar
    else:
        day = monthrange(int(anio), int(meses[mes]))[1] # el maximo de dias va a ser los que tenga el mes
    for line in content:
        #print (datamatutino)
        if "pdf" in line:
            linebef = line.split("a href=\"")[1] # capturar el inicio de la URL
            URL = linebef.split("\" class=")[0]  # capturar la URL completa
            #print (URL)
            filename = URL.split("/")[-1]
            filedate = re.split('_|-',filename) # fecha en el archivo
            if len(filedate[0]) == 1: # si el dia en el archivo viene con un solo digito
                filename = "0" + filename
            if day > int(filedate[0]):
                day = day - 1
            if "MATUTINO" in filename.upper():
                if day == int(filedate[0]):
                    print(datamatutino[0], datamatutino[1])  # corregir a futuro 
                    urlretrieve(datamatutino[0], datamatutino[1])
                datamatutino = [URL, filename]
            else:
                if day == int(filedate[0]):
                    print(URL + ", " + filename)
                    urlretrieve(URL, filename)
                    day = day - 1









