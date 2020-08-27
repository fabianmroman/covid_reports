# Section 1 - Loading our Libraries
import pandas as pd
from datetime import datetime

def dTime (caseslist):
    """ Expects a list and returns a list """
    listadup=[]; i=0; j=1

    for l in caseslist:
        if l==0:
            listadup.append(0)
        elif l==1: 
            if caseslist[i-j]==0:
                listadup.append(1)
            else:
                listadup.append(0)
        else:
            j=1
            while l/2 < caseslist[i-j]:
                j=j+1
            listadup.append(j)
        i=i+1
    return listadup

# Section 2 - Loading and Selecting Data
#df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])

# I will use local data by now

df = pd.read_csv('countries-aggregated.csv', parse_dates=['Date'])



country = input ("Select a country: ")

countries = [country] # This MUST be a list


df = df[df['Country'].isin(countries)] # This is the filter. Match btw "Country" and list
# "df['Country'].isin(countries)" is a special bool from pandas. If True, includes the line
# class 'pandas.core.series.Series'

# Section 3 - Creating a Summary Column
# df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
# Sum three values and put in the end

# Corrected, Active column
df = df.assign(Active=lambda y: df.Confirmed - df.Recovered - df.Deaths)

auxlist = df['Confirmed']
auxlist = list (auxlist)
duplist = dTime (auxlist)
df['Tiempodupl'] = duplist

# Change index
df = df.set_index('Date')

# Delete country column

df = df.drop(columns=['Country'])

# Save to csv

csv_filename = country + ".csv"
excel_filename = country + ".xlsx"

#df.to_csv(csv_filename)
# Is a method from pandas!!! (pd, not df)
writer = pd.ExcelWriter(excel_filename, datetime_format='DD/MM/YYYY')
df.to_excel (writer)
writer.save()
