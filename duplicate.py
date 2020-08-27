"""
Este script genera un archivo Excel con datos del COVID-19 por cada pais seleccionado. Utiliza el siguiente dataset:
https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv


CHANGELOG

v1.0 Reporte adaptado a partir de https://towardsdatascience.com/visualizing-covid-19-data-beautifully-in-python-in-5-minutes-or-less

v1.1 Se pueden seleccionar varios paises. 
     Added duplication time for Active, Recovered and Confirmed. Rewritten dTime function
	
v1.2 Funcion que calcula el Tiempo de Duplicacion reescrita.
     Se puede calcular el tiempo de duplicacion de varias columnas.

v1.3 Agregadas nuevas columnas para mostrar mas indicadores

v1.4 Reorganizados nombres de variables y comentarios para darle legibilidad y coherencia al codigo.
     Codigo adaptado con paths diferentes para cada tipo de archivo.
     Calculo indice de mortalidad. Renombrado de columnas.
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


df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
country = input ("Seleccionar uno o varios paises separados por comas, con o sin espacios: ")
countries = country.split(",")  # This MUST be a list
redondeo = 4  # Cuantos digitos decimales se desean para los indicadores

for country in countries:
    country = country.strip()
    countryselected = [country]
    dfcountry = df[df['Country'].isin(countryselected)]  # special bool from pandas. If True, includes the line
    dfcountry.rename(columns={"Date": "Fecha", "Confirmed": "Confirmados", "Recovered": "Recuperados", "Deaths": "Muertos"}, inplace=True) # Rename

    # Calcular y agregar columna de activos
    dfcountry = dfcountry.assign(Activos=lambda y: df.Confirmed - df.Recovered - df.Deaths) 
    lconfirmed = dfcountry.Confirmados.to_list() # Se usa para calcular otros indicadores

    # Casos nuevos
    i=1
    nuevos = []
    nuevos.append(0) # el primer dia nunca va a tener contra que compararse
    while i < len(lconfirmed):
        nuevos.append(lconfirmed[i] - lconfirmed[i-1])
        i+=1
    dfcountry.insert(1, "Nuevos", nuevos)

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

    print (dfcountry)

    # Mortalidad
    dfcountry = dfcountry.assign(Mortalidad=lambda y: round(dfcountry.Muertos / dfcountry.Activos,redondeo)*100)
    dfcountry.rename(columns={"Mortalidad": "%Mortalidad"}, inplace=True)

    # Change index
    dfcountry = dfcountry.set_index('Fecha')

    # Delete country column
    dfcountry = dfcountry.drop(columns=['Country'])

    # Save to Excel file
    excel_filename = "./xlsx/" + country + ".xlsx"
    writer = pd.ExcelWriter(excel_filename, datetime_format='DD/MM/YY') # Is a method from pandas!!! (pd, not df)
    dfcountry.to_excel (writer)
    writer.save()
