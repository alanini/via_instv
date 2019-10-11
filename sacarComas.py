import os
import pandas
import re

files = [i for i in os.listdir(".") if i.endswith("csv")]
#files = ['C:\\Rocking Data\\Clientes\\Viacom\\WebScraping\\subida16082019.csv']
for archivo in files:
    print(archivo)
    
    entrada=open(archivo,"r",encoding="utf8")
    salida=open("salida"+archivo,"w",encoding="utf8")
    contador=0
    for fila in entrada:
        if len(fila.split(","))==10:
            #salida.write(fila)
            registro=fila.split(",")[0]
            if(registro=="telefenoticias"):
                pass
            else:
                print(contador,registro)
            #pass
        else:
            itera=0
            cadena=""
            for palabra in fila.split(","):
                if itera>4 and itera<len(fila.split(","))-4:
                    cadena+=palabra
                else:
                    if(itera==len(fila.split(","))-3):
                        cadena+=","+palabra+","
                    else:
                        cadena+=palabra+","
                itera+=1
            salida.write(cadena)

            print(len(fila.split(",")),contador)
        contador=contador+1



