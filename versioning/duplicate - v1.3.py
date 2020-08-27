"""
v1.1 - ver fecha 
    Added support to select several countries.
    Added duplication time for Active, Recovered and Confirmed. Rewritten dTime function
	
v1.2 Updated dTime function (using from province report)

v1.3 Agregadas nuevas columnas para procesar datos (ver que es lo que ya esta hecho en Github)
"""

import pandas as pd

def dTime (df, *from_columns):
    """ Receives a Dataframe. Returns a DataFrame with duplication time columns
    from selected items in parameters"""

    for column in from_columns:
        columnlist = df[column]       # Get the column
        columnlist = list(columnlist) # Cast DataFrame to a list 

        duplist=[]; i=0; j=1   # Inicialization
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
                    j="N/A"
                else:
                    while l/2 < columnlist[i-j] and j<=i:
                        j=j+1
                duplist.append(j)       
            i=i+1
        df['Tiempodupl' + column] = duplist
    return df

# I will use local data by now
df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
#df = pd.read_csv('countries-aggregated.csv', parse_dates=['Date'])



country = input ("Select a country, our countries separated by commas without spaces: ")
#country = "Argentina"
countries = country.split(",")  # This MUST be a list

for country in countries:
    # Convert country in a list of a single object - Pandas just allow lists
    # as parameters. Using countryselected as variable. 
    countryselected = [country]
    dfcountry = df[df['Country'].isin(countryselected)] # This is the filter. Match btw "Country" and list
    # "dfcountry['Country'].isin(countryselected)" is a special bool from pandas. If True, includes the line
    # class 'pandas.core.series.Series'
    # df is the original DataFrame, dfcountry is the one selected inside the for loop
    
    # Corrected, Active column
    dfcountry = dfcountry.assign(Active=lambda y: df.Confirmed - df.Recovered - df.Deaths)

    lconfirmed = dfcountry.Confirmed.to_list()

    # Casos nuevos
    i=1
    nuevos = []
    nuevos.append(0) # el primer dia nunca va a tener contra que compararse
    while i < len(lconfirmed):
        nuevos.append(lconfirmed[i] - lconfirmed[i-1])
        i+=1

    dfcountry.insert(1, "Nuevos", nuevos)

    # % de Casos nuevos
    i=1
    porcentnuevos = []
    porcentnuevos.append("N/A") # el primer dia nunca va a tener contra que compararse
    while i < len(lconfirmed):
        try:
            porcentnuevos.append(lconfirmed[i] / lconfirmed[i-1])
        except:
            porcentnuevos.append("N/A")
        i+=1

    dfcountry.insert(4, "%Diario", porcentnuevos)

    # Tendencia de casos nuevos
    i=1
    tendencianuevos = []
    tendencianuevos.append("N/A") # el primer dia nunca va a tener contra que compararse
    while i < len(nuevos):
        try:
            tendencianuevos.append(nuevos[i] / nuevos[i-1])
        except:
            tendencianuevos.append("N/A")
        i+=1

    dfcountry.insert(5, "Tendencia Nuevos", tendencianuevos)


    

    dfcountry = dTime (dfcountry, "Confirmed", "Recovered", "Active")

    # Change index
    dfcountry = dfcountry.set_index('Date')

    # Delete country column
    dfcountry = dfcountry.drop(columns=['Country'])

    # Save to Excel file
    excel_filename = country + ".xlsx"

    #df.to_csv(csv_filename)
    # Is a method from pandas!!! (pd, not df)
    print (dfcountry)
    writer = pd.ExcelWriter(excel_filename, datetime_format='DD/MM/YY')
    dfcountry.to_excel (writer)
    writer.save()
