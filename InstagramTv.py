#!/usr/bin/python3
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from datetime import datetime
import re
import os
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 

chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.binary_location = "/usr/bin/google-chrome-stable"


def extraerDatos(content,titulos,canal):
   driver2 = webdriver.Chrome(executable_path='/usr/bin/chromedriver',   chrome_options=chrome_options)	
   hoy= datetime.now().strftime('%Y-%m-%d')
   archivo_salida = open("/IGTV/archivos/"+canal+hoy+".csv","w",encoding="utf8")
   print(content,titulos)
   lista_visitas = []
   contador=0
    
   archivo_salida.write("canal,fecha_carga,fecha_creacion,url,titulo,comentario,duracion,likes,reproducciones,comentarios\n")

   for web in content:
        lista_elemento=[]
        driver2.get(web)
        time.sleep(2) 
        source = driver2.page_source
        data=bs(source, 'html.parser')
        #scripts = data.html.find_next_sibling("script")
        visitas = data.findAll("span", class_= "vcOH2")
        for visita in visitas:
            print(web,"visitas:",visita.text)
        fecha_creacion= data.findAll("time")
        for fecha in fecha_creacion:
            dia=fecha.get("datetime")
            break
        tituloco = data.find_all("span", class_="Linkify")
        for texto in tituloco:
            comentario=texto.text
            print(comentario)
        scripts = data.findAll("script")
        #print(scripts)
        for codigo in scripts:
            if str(codigo.text).find("graphql")>0:
                try:
                    texto=str(codigo.text).split("window._sharedData = ")[1]
                    estadisticas=json.loads(texto[:-1])
                    dia=str(dia).split("T")[0]
                    vistas=estadisticas['entry_data']['PostPage'][0]['graphql']['shortcode_media']['video_view_count']
                    likes=estadisticas['entry_data']['PostPage'][0]['graphql']['shortcode_media']["edge_media_preview_like"]["count"]
                    comentarios=estadisticas['entry_data']['PostPage'][0]['graphql']['shortcode_media']["edge_media_preview_comment"]["count"]
                    titular = estadisticas['entry_data']['PostPage'][0]['graphql']['shortcode_media']["title"]
                    #print(estadisticas['entry_data']['PostPage'][0]['graphql']['shortcode_media']["video_duration"])
                    duracion = str(estadisticas['entry_data']['PostPage']['graphql']['shortcode_media']["video_duration"])
                except:
                    print("fallo la conversion")   
                    duracion=0

            else:
                if(str(codigo.text).find("@context")>0):
                    estadisticas=json.loads(codigo.text)
                    dia=str(dia).split("T")[0]
                    print("eligio opcion 2")
                    print(estadisticas)
                    contenido=estadisticas["description"].split(",")
                    vistas=contenido[0]
                    likes=estadisticas["interactionStatistic"]["userInteractionCount"]
                    comentarios=estadisticas["commentCount"]
                    try:
                        duracion=estadisticas["video_duration"]
                    except:
                        duracion=0 #estadisticas["video_duration"]
                    try:
                        titular= estadisticas["caption"]
                    except:
                        titular=contenido[1]
        
        try:
            lista_elemento.append([canal,hoy,dia,web,str(titular).replace(',',' '),str(comentario).replace(',','').replace('"',''),duracion,likes,vistas,comentarios])
            archivo_salida.write(canal+ "," + hoy + "," + dia +","+ web + "," + str(titular).replace(',',' ').replace("\"","")+","+ str(comentario).replace(",","").replace("\n","").replace("\"","") +","+ str(duracion) +","+ str(likes) +"," + str(vistas) + "," + str(comentarios) +"\n")
            contador=contador+1
            lista_visitas.append(lista_elemento)
        except:
            contador+=1
            print("hubo un error cargando",canal,str(contador))
   archivo_salida.close()
   print("termino un loop")
   driver2.close()
   return lista_visitas

def procesoSelenium(script):
   links=[]
   lista_titulos = []
   for link in script.findAll('a', class_="_bz0w"):
     lista_titulos.append(link.text)
     links.append('https://www.instagram.com'+link.get('href'))
     time.sleep(0.5) 
   return links,lista_titulos

if __name__ == '__main__':
   driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',   chrome_options=chrome_options)
   usernameList = ['mtvla','mtvbrasil','telefe','telefenoticias','nickelodeonbr','comedycentralla','comedycentralbr','mundonick','teleferosario','telefesantafe','telefecordoba','telefetucuman','telefesalta','telefeneuquen','telefemardelplata','victoriatelefe']
   #usernameList = ['telefe','telefenoticias','nickelodeonbr','comedycentralla','comedycentralbr','mundonick','teleferosario','telefesantafe','telefecordoba','telefetucuman','telefesalta','telefeneuquen','telefemardelplata','victoriatelefe']
   #usernameList = ['mtvla','mtvbrasil']
   for i in usernameList:   
        #procesoSelenium(i)
        titulos_maestro=[]
        contenido_maestro=[]
        canal='https://www.instagram.com/' + i + '/channel/'
        print(canal)
        driver.get(canal)
        time.sleep(2) 
        
        # manejo de scrolling
        SCROLL_PAUSE_TIME = 1.5
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            source = driver.page_source
            data=bs(source, 'html.parser')
            script_ = data.find('body')
            contenido,titulos=procesoSelenium(script_)
            for elemento in contenido:
                contenido_maestro.append(elemento)
            for titulo in titulos:
                titulos_maestro.append(titulo)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        
        #
        #Me quedo con los unicos
        unq_contenido_maestro=list(set(contenido_maestro))
        unq_titulos_maestro=list(set(titulos_maestro))
        print(len(unq_contenido_maestro),len(unq_titulos_maestro))
        tabla_canal=extraerDatos(unq_contenido_maestro,unq_titulos_maestro,i) 
    
   print(tabla_canal)
   driver.close()    
