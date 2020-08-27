# Section 1 - Loading our Libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker

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
df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
countries = ['Argentina'] # This MUST be a list
print (df)
print (countries)
df = df[df['Country'].isin(countries)] # This is the filter. Match btw "Country" and list
# "df['Country'].isin(countries)" is a special bool from pandas. If True, includes the line
# class 'pandas.core.series.Series'
print (df)

# Section 3 - Creating a Summary Column
# df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
# Sum three values and put in the end

# Corrected, Active column
df = df.assign(Active=lambda y: df.Confirmed - df.Recovered - df.Deaths)

auxlist = df['Confirmed']
auxlist = list (auxlist)
duplist = dTime (auxlist)
df['Tiempodupl'] = duplist

print (df)



covid = df.pivot(index='Date', columns='Country')

print (covid)

colors = {'Active':'#045275', 'Confirmed':'#089099', 'Recovered':'#7CCBA2', 'Deaths':'#FCDE9C'}
plt.style.use('fivethirtyeight')

plot = covid.plot(figsize=(12,8), color=list(colors.values()), linewidth=5, legend=False)
plot.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
plot.grid(color='#d4d4d4')
plot.set_xlabel('Date')
plot.set_ylabel('# of Cases')

# Section 8 - Assigning Colour
for country in list(colors.keys()):
    plot.text(x = covid.index[-1], y = covid[country].max(), color = colors[country], s = country, weight = 'bold')

plt.show()
plt.savefig("temp.png")
