__author__ = 'RAMOSVACCA'

#from xml.etree import cElementTree as ET
import os
import xml.etree.ElementTree as ET
from variosaltiempo import hacerlista_desdexml
from threading import Thread
import math

#archivoxml = '/Volumes/Ramosvacca/Github/geolocarti/XML/xmlunivalleoriginal.xml'
#archivoxml = '/media/ramosvacca/A-P-IDRV/Github/geolocarti/XML/Scopus_geolocation.xml'
archivoxml = '/media/ramosvacca/A-P-IDRV/Github/geolocarti/XML/xmlunivalle.xml'

f=open(archivoxml)
rr=f.read()
#print(rr)

mis_nodos = []
mis_vertices = []
articulos  = []

def obtener_metadatos(xml, campos, nodos, vertices, hilos):
        contador = 0
        tree = ET.parse(xml)
        print(tree)
        root = tree.getroot()
        print(root)
        print('INICIAMOS ----')
        for child_entry in root: #Cada entry
            print('Entry---->', contador)
            afiliaciones_entry = []
            vertices_entry = []
            for campito in child_entry: # Cada campo dentro de entry
                local_afiliacion=[]
                #print (campito.tag)
                if campito.tag == campos: #Si el campo de entry coincide con el de entrada #affiliation
                    print('- INICIO extraccion de info de affil')
                    local_name = 0
                    local_city = 0
                    local_country = 0
                    for llegando in campito: #Entonces, para cada subcampo en #affiliation
                        #print(llegando.tag)
                        if llegando.tag == '{http://www.w3.org/2005/Atom}affilname': #Si es un #affilname, haga algo
                            #print('.',llegando.text)
                            local_name = str(llegando.text)
                            #print(local_name)
                            if local_name != 'None':
                                """for llegando in campito:
                                    if llegando.tag == '{http://www.w3.org/2005/Atom}afid':
                                        local_name = str(llegando.text)
                                        afiliaciones_entry += [local_name]
                            else:"""

                                local_name = local_name.strip()
                        if llegando.tag == '{http://www.w3.org/2005/Atom}affiliation-city':
                            local_city = str(llegando.text)
                            local_city = local_city.strip()
                        if llegando.tag == '{http://www.w3.org/2005/Atom}affiliation-country':
                            local_country = str(llegando.text).strip()
                    local_afiliacion += [local_name, local_city, local_country]
                    #print(local_afiliacion)
                    print('-- FIN extraccion ')
                    if len(local_afiliacion)>0:
                        print('-- INICIO Anexar')
                        control = 0
                        for i in afiliaciones_entry:
                            if i[0] == local_afiliacion[0]:
                                i[3]+= 1
                                control = 1
                        if control == 0:
                            afiliaciones_entry += [local_afiliacion+[1]]
                        print('-- FIN Anexar')
            print('afilcentry')

            if len(afiliaciones_entry)<20000000000:

                def nodoshilos(pedazo, control, afil):
                    if len(pedazo)>0:
                        for nodo in pedazo:
                            if nodo[0] == afil[0]:
                                control = 1
                                nodo[3] += afil[3]

                for c_afil in afiliaciones_entry:
                    chunksize = int(math.ceil(len(nodos) / float(hilos[0])))
                    threads = []
                    control =0
                    for i in range(hilos[0]):
                        t = Thread(
                            target=nodoshilos,
                            args=(nodos[chunksize * i:chunksize * (i+1)],
                                  control, c_afil))
                        threads.append(t)
                        t.start()

                    for t in threads:
                        t.join()

                    if control==0:
                        nodos += [c_afil]

                largo = len(afiliaciones_entry)



                print('inicia entry vertices', contador)
                for i in range(0, largo):
                    for j in range(i+1, largo):

                        if (([afiliaciones_entry[i][0], afiliaciones_entry[j][0]] not in vertices_entry)
                            or ([afiliaciones_entry[j][0], afiliaciones_entry[i][0]] not in vertices_entry)):

                                vertices_entry += [[afiliaciones_entry[i][0], afiliaciones_entry[j][0]]]

                print('termina entrey certices', contador)

                def verticesaux(algo, control, mi_vertice):
                    if (([mi_vertice[0], mi_vertice[1]] == algo) or ([mi_vertice[1], mi_vertice[0]] == algo)):
                                control = 1

                def verticeshilos(pedazo, control, vert): #Le entra un pedazo de matriz, una variable binaria, un vertice.
                    if len(pedazo)>0:
                        hilosdentro = []
                        for vertice in pedazo:
                            h = Thread(                 #descompone la matriz, un hilo por elemento. Compara si ese elemento es igual al vertice
                                target=verticesaux,
                                args=(vertice, control, vert)
                            )
                            hilosdentro.append(h)
                            h.start()
                        for h in hilosdentro:
                            h.join()


                if len(vertices_entry)<2000000000000:
                    print('- Indexar vertices a lista general')
                    veamos = 0
                    total = len(vertices_entry)
                    for vertice in vertices_entry:
                        if veamos%10==0:
                            print('vertice ', veamos, ' de ', total)
                        chunksize = int(math.ceil(len(vertices) / float(10)))
                        threads = []
                        control =0
                        for i in range(4):
                            t = Thread(
                                target=verticeshilos,
                                args=(vertices[chunksize * i:chunksize * (i+1)],
                                      control, vertice)
                            )
                            threads.append(t)
                            t.start()
                        for t in threads:
                            t.join()

                        if control == 0:

                            vertices += [vertice]

                        veamos += 1
                    print('- FIN DE TODO')
            contador += 1
            #print(afiliaciones_entry)
            #print('SIGUIENTE')


        #print('Fin')


print(obtener_metadatos(archivoxml, '{http://www.w3.org/2005/Atom}affiliation', mis_nodos, mis_vertices, [10]))
print('Mis vertices:', len(mis_vertices), mis_vertices)
print('Mis Nodos:', len(mis_nodos), mis_nodos)

mis_nodos_coord = hacerlista_desdexml(mis_nodos, 20)

path = os.path.abspath('ge.txt')
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

