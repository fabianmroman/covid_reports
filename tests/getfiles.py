import pandas
#import urllib.request
from urllib.request import * #Request, urlopen, urlretrieve
from datetime import date


meses = ("abril", "mayo", "junio", "julio")
anio = "2020"
today = date.today()
today = today.strftime("%d-%m-%Y")

print (today)

opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
install_opener(opener)

for mes in meses:
    req = Request('https://www.argentina.gob.ar/coronavirus/informe-diario/' + mes + anio, headers={'User-Agent': 'Mozilla/5.0'})
    content = urlopen(req).read()
    content = content.decode('utf-8') # convert to a string
    content = content.split("><")
    for line in content:
        if "pdf" in line:
            linebef = line.split("a href=\"")[1]
            URL = linebef.split("\" class=")[0]
            print(URL)
            print ("---------------------------------------")
            filename = URL.split("/")[-1]
            #urlretrieve(URL, filename)








