import pandas
#import urllib.request
from urllib.request import Request, urlopen
from urllib import urlretrieve
from datetime import date


meses = ("abril", "mayo", "junio", "julio")
today = date.today()
today = today.strftime("%d-%m-%Y")

print (today)


req = Request('https://www.argentina.gob.ar/coronavirus/informe-diario/julio2020', headers={'User-Agent': 'Mozilla/5.0'})
content = urlopen(req).read()
content = content.decode('utf-8') # convert to a string



urlretrieve ("https://www.argentina.gob.ar/sites/default/files/05-07-20-reporte-vespertino-covid-19.pdf", "05-07-20-reporte-vespertino-covid-19.pdf")


content = content.split("><")
for line in content:
    if "pdf" in line:
        linebef = line.split("a href=\"")[1]
        URL = linebef.split("\" class=")[0]
        print(URL)
        print ("---------------------------------------")
