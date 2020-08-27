import pandas as pd
import os
import sys

    # chequear que exista el archivo de provincias y que comience en una fecha mayor al 31/03 y comenzar (pasar fecha)
    # si comienza en otra fecha y existe el archivo provincias_marzo.csv copiarlo a provincias.csv y comenzar (pasar fecha)
    # si no existe el archivo de marzo o si el archivo de provincias comienza <> al 31/03
    # lo baja desde Github! 
    
provFile = False
provmarzoFile = False

# Chequear existencia del archivo csv con el dataset 
try:
    with open('provincias.csv', 'r') as f:
        provFile = True
        f.close()
except:
    pass

try:
    with open('provincias_marzo.csv', 'r') as g:
        provmarzoFile = True
        g.close()
except:
    pass

print (provFile)
print (provmarzoFile)
