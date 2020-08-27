"""
v1.1 - ver fecha 
    Added support to select several countries.
    Added duplication time for Active, Recovered and Confirmed. Rewritten dTime function
	
v1.2 Updated dTime function (using from province report)
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

    dfcountry = dTime (dfcountry, "Confirmed", "Recovered", "Active")

    # Change index
    dfcountry = dfcountry.set_index('Date')

    # Delete country column
    dfcountry = dfcountry.drop(columns=['Country'])

    # Save to Excel file
    excel_filename = country + ".xlsx"

    #df.to_csv(csv_filename)
    # Is a method from pandas!!! (pd, not df)
    writer = pd.ExcelWriter(excel_filename, datetime_format='DD/MM/YYYY')
    dfcountry.to_excel (writer)
    writer.save()
