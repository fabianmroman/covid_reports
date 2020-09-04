"""
Este script genera un archivo Excel con datos del COVID-19 por cada provincia seleccionada. Utiliza el dataset generado
por el script sortfilenames.py. Antes de ejecutar este script ejecutar dicho script para disponer
de datos actualizados.


    CHANGELOG
    v1.0 Script para generar reportes de provincias a partir del dataset del pais.

    v1.1
    Funcion que calcula el Tiempo de Duplicacion reescrita. 
    Se puede calcular el tiempo de duplicacion de varias columnas.

    v1.2
    Reorganizados nombres de variables y comentarios para darle legibilidad y coherencia al codigo.
    Codigo adaptado con paths diferentes para cada tipo de archivo.

    v1.2.1
    Se corrige nombres de provincias en caso de introducirlas de diferente forma.
"""

import pandas as pd
pd.options.mode.chained_assignment = None 

CSV_FILE = "./csv/provincias.csv"


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

def corregirTipeo (provincia):
    equivalencia = ""
    listado = {"Cordoba": "Córdoba", "Tucuman": "Tucumán", "Pcia de Buenos Aires": "Buenos Aires",
               "Provincia de Buenos Aires": "Buenos Aires", "CABA": "Ciudad de Buenos Aires",
               "Ciudad Buenos Aires": "Ciudad de Buenos Aires", "Entre Rios": "Entre Ríos",
               "Neuquen": "Neuquén", "Rio Negro": "Río Negro", "Tucuman": "Tucumán"}
    try:
        equivalencia = listado[provincia]
    except:
        return provincia
    if equivalencia != "":
        return equivalencia


# MAIN
# ====

df = pd.read_csv(CSV_FILE, encoding="utf-16") # Encoding para ver los acentos en Excel

seleccion = input ("Seleccionar una o varias provincias separadas por comas, con o sin espacios: ")
provincias = seleccion.split(",")
print (provincias)


for provincia in provincias:
    provincia = provincia.strip()
    provincia = corregirTipeo(provincia) # Corrige en caso de introducir las provincias de != formas
    print (provincia)
    provinciaseleccionada = [provincia] # Debe ser una lista para buscar en el dataset
    dfprovincia = df[df['Provincia'].isin(provinciaseleccionada)]
    dfprovincia = dTime (dfprovincia, "Acumulado") # Agregar columna de T. de Duplicacion
    dfprovincia = dfprovincia.set_index('Fecha') # Cambiar indice
    dfprovincia = dfprovincia.drop(columns=['Provincia']) # Borrar columna de provincia 

    # Guardar a Excel 
    excel_filename = "./xlsx/" + provincia + ".xlsx"
    writer = pd.ExcelWriter(excel_filename, datetime_format='DD/MM/YYYY') # ExcelWriter es de Pandas! 
    dfprovincia.to_excel (writer)
    writer.save()
