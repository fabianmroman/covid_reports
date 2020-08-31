"""
Este script genera un archivo Excel con datos del COVID-19 por cada pais seleccionado. Utiliza los datasets globales
disponibles en humdata.org. En versiones anteriores a la 1.5 se utilizaba un dataset en base de este, pero dejo de
actualizarse


CHANGELOG

v1.0 Reporte adaptado a partir de https://towardsdatascience.com/visualizing-covid-19-data-beautifully-in-python-in-5-minutes-or-less-affc361b2c6a

v1.1 Se pueden seleccionar varios paises. 
     Added duplication time for Active, Recovered and Confirmed. Rewritten dTime function
	
v1.2 Funcion que calcula el Tiempo de Duplicacion reescrita.
     Se puede calcular el tiempo de duplicacion de varias columnas.

v1.3 Agregadas nuevas columnas para mostrar mas indicadores

v1.4 Reorganizados nombres de variables y comentarios para darle legibilidad y coherencia al codigo.
     Codigo adaptado con paths diferentes para cada tipo de archivo.
     Calculo indice de mortalidad. Renombrado de columnas.
     
v1.5 Comienzan a utilizarse los datasets globales de humdata.org, ya que los que se utilizaron en el script original
     dejaron de actualizarse. Adaptacion del codigo a los nuevos datasets.
     https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/
     Solucionados issues con tipos de datos con el nuevo dataset. 
"""

import pandas as pd

def dTime (df, *from_columns):
    """ Recibe un dataframe. Devuelve un dataframe con las columnas de tiempo de duplicacion recibidas
        por parametro. Se utiliza el metodo simetrico. 
    """

    for column in from_columns:
        columnlist = df[column] 
        columnlist = list(columnlist) # DataFrame -> List

        duplist=[]; i=0; j=1
        for l in columnlist:
            if l==0:
                duplist.append(0)
            elif l==1: 
                if columnlist[i-j]==0:
                    duplist.append(1)
                else:
                    duplist.append(0)
            else:
                j=1
                if l/2 < columnlist[0]:
                    j=""
                else:
                    while l/2 < columnlist[i-j] and j<=i:
                        j=j+1
                duplist.append(j)       
            i=i+1
        df['Tiempodupl' + column] = duplist
    return df

# Dataset antiguo 
#df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
#datetime.utcnow()

# Carga de dataset globales
dfconfirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
dfdeaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
dfrecovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

country = input ("Seleccionar uno o varios paises separados por comas, con o sin espacios: ")
countries = country.split(",")  # This MUST be a list
redondeo = 4  # Cuantos digitos decimales se desean para los indicadores

for country in countries:
    country = country.strip()

    #Seleccionar datos
    confirmed = dfconfirmed.loc[dfconfirmed['Country/Region'] == country]
    deaths = dfdeaths.loc[dfdeaths['Country/Region'] == country]
    recovered = dfrecovered.loc[dfrecovered['Country/Region'] == country]

    # Crear el dataset 
    dfcountry = confirmed.append(deaths)
    dfcountry = dfcountry.append(recovered)
    dfcountry = dfcountry.T[4:]
    dfcountry.index.name = "Fecha"
    dfcountry.columns = ['Confirmados', 'Muertos', 'Recuperados']
    dfcountry = dfcountry.astype('int64') # Cambio de tipo de datos para poder hacer las operaciones sin errores

    # Formatear el indice segun el formato de fecha estandar de Python 
    dfcountry.reset_index(level=0, inplace=True)
    dfcountry = dfcountry.rename(columns={'index': 'DateTime'})
    dfcountry['Fecha'] = dfcountry['Fecha'].astype('datetime64')
    dfcountry.index = dfcountry.Fecha
    dfcountry = dfcountry.drop(columns=['Fecha'])
    
    # Calcular y agregar columna de activos
    dfcountry = dfcountry.assign(Activos=lambda y: dfcountry.Confirmados - dfcountry.Muertos - dfcountry.Recuperados) 
    lconfirmed = dfcountry.Confirmados.to_list() # Se usa para calcular otros indicadores

    # Casos nuevos
    i=1
    nuevos = []
    nuevos.append(0) # el primer dia nunca va a tener contra que compararse
    while i < len(lconfirmed):
        nuevos.append(lconfirmed[i] - lconfirmed[i-1])
        i+=1
    dfcountry.insert(0, "Nuevos", nuevos)

    # % de casos nuevos
    i=1
    porcentnuevos = []
    porcentnuevos.append("") # el primer dia nunca va a tener contra que compararse
    while i < len(lconfirmed):
        try:
            porcentnuevos.append(round(lconfirmed[i] / lconfirmed[i-1], redondeo))
        except:
            porcentnuevos.append("")
        i+=1
    dfcountry.insert(4, "Variacion Diaria", porcentnuevos)

    # Tendencia de casos nuevos
    i=1
    tendencianuevos = []
    tendencianuevos.append("") # el primer dia nunca va a tener contra que compararse
    while i < len(nuevos):
        try:
            tendencianuevos.append(round(nuevos[i] / nuevos[i-1], redondeo))
        except:
            tendencianuevos.append("")
        i+=1
    dfcountry.insert(5, "Tendencia Nuevos", tendencianuevos)

    # Tiempo de duplicacion 
    dfcountry = dTime (dfcountry, "Confirmados", "Recuperados", "Activos")

    # Mortalidad
    dfcountry = dfcountry.assign(Mortalidad=lambda y: round(dfcountry.Muertos / dfcountry.Activos,redondeo)*100 )
    dfcountry.rename(columns={"Mortalidad": "%Mortalidad"}, inplace=True)

    print (dfcountry)

    # Guardar a un archivo Excel
    excel_filename = "./xlsx/" + country + ".xlsx"
    writer = pd.ExcelWriter(excel_filename, datetime_format='DD/MM/YY') # Metodo de Pandas, no del dataset!
    dfcountry.to_excel (writer)
    writer.save()
