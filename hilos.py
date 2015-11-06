__author__ = 'RAMOSVACCA'

__author__ = 'RAMOSVACCA'

#from xml.etree import cElementTree as ET
import os
import xml.etree.ElementTree as ET
from variosaltiempo import hacerlista_desdexml
from threading import Thread
import math
import time

#archivoxml = '/Volumes/Ramosvacca/Github/geolocarti/XML/uniprueba.xml'
#archivoxml = '/media/ramosvacca/A-P-IDRV/Github/geolocarti/XML/Scopus_geolocation.xml'
archivoxml = '/media/ramosvacca/A-P-IDRV/Github/geolocarti/XML/uniprueba.xml'

#f=open(archivoxml)
#rr=f.read()
#print(rr)

mis_nodos = []
mis_vertices = []
articulos  = []

def obtener_metadatos(xml, campos, nodos, vertices):
        tiempos = []
        tree = ET.parse(xml)
        root = tree.getroot()
        contador = 0
        for child_entry in root: #Cada entry
            print('Entry---->', contador)
            afiliaciones_entry = []
            for campito in child_entry: # Cada campo dentro de entry
                local_afiliacion=[]
                #print (campito.tag)
                if campito.tag == campos: #Si el campo de entry coincide con el de entrada #affiliation

                    local_name = 0
                    local_city = 0
                    local_country = 0
                    for llegando in campito: #Entonces, para cada subcampo en #affiliation
                        if llegando.tag == '{http://www.w3.org/2005/Atom}affilname': #Si es un #affilname, haga algo
                            local_name = str(llegando.text)
                            if local_name != 'None':
                                local_name = local_name.strip()
                        if llegando.tag == '{http://www.w3.org/2005/Atom}affiliation-city':
                            local_city = str(llegando.text)
                            local_city = local_city.strip()
                        if llegando.tag == '{http://www.w3.org/2005/Atom}affiliation-country':
                            local_country = str(llegando.text).strip()
                    local_afiliacion += [local_name, local_city, local_country]
                    #print(local_afiliacion[0])
                    #print(local_list)

                    if len(local_afiliacion)>0:
                        control = 0
                        for nodo in nodos:
                            #print(nodos)

                            if nodo[0] == local_afiliacion[0]:
                                control = 1
                                nodo[3] += 1

                        if control==0:
                            nodos += [local_afiliacion+[1]]

                        if local_afiliacion not in afiliaciones_entry:
                            afiliaciones_entry += [local_afiliacion]

            def angel(normal,alreves,pedazo, control):
                if ((normal in pedazo) or (alreves in pedazo)):
                    control = 1


            #print('afiliaciones entry', afiliaciones_entry)
            largo = len(afiliaciones_entry)
            if largo > 1:

                #print(afiliaciones_entry)
                start = time.time()
                for i in range(0, largo):
                    if i % 10 == 0:
                        print('vertice ', i, ' de ', largo)
                    for j in range(i+1, largo):
                        der = [afiliaciones_entry[i][0], afiliaciones_entry[j][0]]
                        izq = [afiliaciones_entry[j][0], afiliaciones_entry[i][0]]

                        npedazo = int(math.ceil(len(vertices) / float(1)))
                        hilos = []
                        control = 0
                        for i in range(1):
                            t = Thread(
                                target=angel,
                                args=(der, izq, vertices[npedazo * i: npedazo * (i+1)],
                                      control))
                            hilos.append(t)
                            t.start()
                        for t in hilos:
                            t.join()
                        if control == 0:
                            vertices += [[afiliaciones_entry[i][0], afiliaciones_entry[j][0]]]
                elapsed = (time.time() - start)
                tiempos += [elapsed]
                print ('FIN Entry -->', contador, '. tiempo de', elapsed)

            contador += 1

            #print(afiliaciones_entry)
            #print('SIGUIENTE')


        return tiempos


tiempos = obtener_metadatos(archivoxml, '{http://www.w3.org/2005/Atom}affiliation', mis_nodos, mis_vertices)

#print('Mis vertices:', len(mis_vertices), mis_vertices)
print('Mis Nodos:', len(mis_nodos), mis_nodos)
print(len(mis_vertices))
print(tiempos)

pathvert = os.path.abspath('sisisi.txt')
fvert = open(pathvert, 'w')
fvert.write(str(mis_vertices))

i=0
mis_nodos_coord = hacerlista_desdexml(mis_nodos, 15)

path = os.path.abspath('jajajaja.txt')
f = open(path, 'w')
f.write(str(mis_nodos_coord))

"""path = os.path.abspath('geolocation_1.txt')
f = open(path,'r')
mis_nodos_coord = f.read()
print('mis nodos coord', str(mis_nodos_coord))"""

mis_vertices_coord = []

for vertice in mis_vertices: # Lo que se hace con cada vertice
    vertice_coord = []
    for end in vertice: # Lo que se hace con cada end
        end_coord = []
        for nodo in mis_nodos_coord: #buscar el nombre del end en los nodos
            if end == nodo[0]:
                end_coord = [[nodo[4], nodo[5]]] # Asignar coordenadas
        vertice_coord += end_coord
    mis_vertices_coord += [vertice_coord]


print(len(mis_nodos_coord), mis_nodos_coord)
print(len(mis_vertices_coord), mis_vertices_coord)

from red_mpl import desc_nodos
from ZZ_variasbonito import mplmap

latsmpl = []
lonsmpl = []
nomsmpl = []
vertsmpl = ''

vertsmpl = desc_nodos(mis_nodos_coord, mis_vertices_coord, latsmpl, lonsmpl, nomsmpl)

mplmap(lonsmpl, latsmpl, nomsmpl, vertsmpl, 1)


print(lonsmpl)
print(latsmpl)
print(nomsmpl)
#print(vertsmpl)


path = os.path.abspath('pruebafinal.txt')
f = open(path, 'w')
f.write(vertsmpl)


mplmap(lonsmpl, latsmpl, nomsmpl, vertsmpl, 1)