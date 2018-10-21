__author__ = 'RAMOSVACCA'

#from xml.etree import cElementTree as ET
import os
import xml.etree.ElementTree as ET
from variosaltiempo import hacerlista_desdexml
from threading import Thread
import math
import time
from joblib import Parallel, delayed
import multiprocessing

archivoxml = '/Volumes/Ramosvacca/Github/geolocarti/XML/Scopus_geolocation.xml'
#archivoxml = '/Volumes/Ramosvacca/Github/geolocarti/XML/xmlunivalle.xml'

#archivoxml = '/media/ramosvacca/A-P-IDRV/Github/geolocarti/XML/Scopus_geolocation.xml'
#archivoxml = '/media/ramosvacca/A-P-IDRV/Github/geolocarti/XML/uniprueba.xml'

#f=open(archivoxml)
#rr=f.read()
#print(rr)

mis_nodos = []
mis_vertices = []
articulos  = []

def obtener_metadatos(xml, campos, nodos, verticesfinal):
        vertices = []
        tiempos = []
        tree = ET.parse(xml)
        root = tree.getroot()
        contador = 0
        for child_entry in root: #Cada entry
            #print('Entry---->', contador)
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
                            local_name = local_name.strip()
                        if llegando.tag == '{http://www.w3.org/2005/Atom}affiliation-city':
                            local_city = str(llegando.text)
                            local_city = local_city.strip()
                        if llegando.tag == '{http://www.w3.org/2005/Atom}affiliation-country':
                            local_country = str(llegando.text).strip()

                    local_afiliacion += [local_name, local_city, local_country]

                    if len(local_afiliacion)>0:
                        control = []
                        for nodo in nodos:
                            #print(nodos)

                            if nodo[0] == local_afiliacion[0]:
                                control += 'a'
                                nodo[3] += 1

                        if len(control)<1:
                            nodos += [local_afiliacion+[1]]

                        if local_afiliacion not in afiliaciones_entry:
                            afiliaciones_entry += [local_afiliacion]

            def angel1(normal,pedazo,control):
                if (normal in pedazo):
                    control += 'a'
                    #print('TRUEEEEEEE', contador)

            def lastry(pedazo, validar):
                if validar == pedazo:
                    return 1
                else:
                    return 0

            largo = len(afiliaciones_entry)
            if largo < 3000000:
                if largo > 1:
                    afiliaciones_entry.sort()
                    #print(afiliaciones_entry)
                    start = time.time()
                    for i in range(0, largo):
                        if i % 10 == 0:
                            print('Afiliacion ', i, ' de ', largo)
                        for j in range((i+1), largo):
                            if i < largo:

                                der = [afiliaciones_entry[i][0], afiliaciones_entry[j][0]]

                                num_cores = multiprocessing.cpu_count()
                                chunksize = int(math.ceil(len(vertices) / float(num_cores)))
                                print(num_cores)
                                inputs=range(len(vertices))
                                if len(vertices) > 0:

                                    control = Parallel(n_jobs=num_cores)(delayed(lastry)(vertices[i], der) for i in inputs)

                                    print(control)

                                if len(control) < 1:
                                    vertices += [der]
                        #print('fin hilos---', contador, ' de ', largo, '\n')

                    elapsed = (time.time() - start)
                    tiempos += [elapsed]
                    print ('FIN Entry -->', contador, '. tiempo de', elapsed)

            contador += 1

            #print(afiliaciones_entry)
            #print('SIGUIENTE')
        #
        verticesfinal += vertices
        return tiempos


tiempos = obtener_metadatos(archivoxml, '{http://www.w3.org/2005/Atom}affiliation', mis_nodos, mis_vertices)

#print('Mis vertices:', len(mis_vertices), mis_vertices)
#print('Mis Nodos:', len(mis_nodos))#, mis_nodos)
#print(tiempos)

mis_nodos.sort()
for i in mis_nodos:
    print(i)
print(len(mis_nodos))

mis_vertices.sort()
for i in mis_vertices:
    print(i)
print(len(mis_vertices))


# pathvert = os.path.abspath('sisisi.txt')
# fvert = open(pathvert, 'w')
# fvert.write(str(mis_vertices))
# print(mis_vertices)
#
# mis_nodos_coord = hacerlista_desdexml(mis_nodos, 10)
#
# path = os.path.abspath('jajajaja.txt')
# f = open(path, 'w')
# f.write(str(mis_nodos_coord))
#
#
#
# """path = os.path.abspath('geolocation_1.txt')
# f = open(path,'r')
# mis_nodos_coord = f.read()
# print('mis nodos coord', str(mis_nodos_coord))"""
#
# mis_vertices_coord = []
#
# for vertice in mis_vertices: # Lo que se hace con cada vertice
#     vertice_coord = []
#     for end in vertice: # Lo que se hace con cada end
#         end_coord = []
#         for nodo in mis_nodos_coord: #buscar el nombre del end en los nodos
#             if end == nodo[0]:
#                 end_coord = [[nodo[4], nodo[5]]] # Asignar coordenadas
#         vertice_coord += end_coord
#     mis_vertices_coord += [vertice_coord]
#
#
# print(len(mis_nodos_coord), mis_nodos_coord)
# print(len(mis_vertices_coord), mis_vertices_coord)
#
# from red_mpl import desc_nodos
# from ZZ_variasbonito import mplmap
#
# latsmpl = []
# lonsmpl = []
# nomsmpl = []
#
# vertsmpl = desc_nodos(mis_nodos_coord, mis_vertices_coord, latsmpl, lonsmpl, nomsmpl)
#
# mplmap(lonsmpl, latsmpl, nomsmpl, vertsmpl, 1)
#
#
# print(lonsmpl)
# print(latsmpl)
# print(nomsmpl)
# #print(vertsmpl)
#
#
# path = os.path.abspath('pruebafinal.txt')
# f = open(path, 'w')
# f.write(vertsmpl)
