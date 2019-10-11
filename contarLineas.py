#!/usr/bin/python3
import os
import shutil
def main():
   files = [i for i in os.listdir("/IGTV/archivos") if i.endswith("csv")]
   for archivo in files:
       counter=0
       print(archivo)
       archi=open("/IGTV/archivos/"+archivo,"r")
       for linea in archi:
           counter+=1
       print(counter)
       if counter>1:
           pass
       else:
           shutil.move("/IGTV/archivos/"+archivo,"/IGTV/historico/"+archivo)
       print(archivo)


if __name__ == "__main__":
    main()
