#!/usr/bin/python3
import datetime
hora=datetime.datetime.now()

FILETO=open("/IGTV/archivos/test.txt","w")
print("esto es una prueba")
FILETO.write(hora.strftime("%d-%m-%Y %H-%M"))
FILETO.close()

