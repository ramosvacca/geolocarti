__author__ = 'RAMOSVACCA'

#from xml.etree import cElementTree as ET
import os
import xml.etree.ElementTree as ET
from variosaltiempo import hacerlista_desdexml

#archivoxml = '/Volumes/Ramosvacca/Github/geolocarti/XML/.xml'
#archivoxml = '/media/ramosvacca/A-P-IDRV/Github/geolocarti/XML/Scopus_geolocation.xml'
archivoxml = '/media/ramosvacca/A-P-IDRV/Github/geolocarti/XML/xmlunivalle.xml'

f=open(archivoxml)
rr=f.read()
#print(rr)

mis_nodos = []
mis_vertices = []
articulos  = []

def obtener_metadatos(xml, campos, nodos, vertices):
        tree = ET.parse(xml)
        root = tree.getroot()
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

                control = 0
                if len(local_afiliacion)>0:
                    for nodo in nodos:
                        #print(nodos)
                        """print('nodo',nodo)
                        print('nodo[0]',nodo[0])
                        print('afiliacion', local_afiliacion[0])"""
                        if nodo[0] == local_afiliacion[0]:
                            control = 1
                            nodo[3] += 1
                if control==0 and len(local_afiliacion):
                    nodos += [local_afiliacion+[1]]

                if len(local_afiliacion)>0:
                    afiliaciones_entry += [local_afiliacion]


            largo = len(afiliaciones_entry)
            if largo>0: #Para cada entry construye unos vertices y nodos, si no existen ya.
                for i in range(0, largo):
                    for j in range(i+1, largo):
                        if (([afiliaciones_entry[i][0], afiliaciones_entry[j][0]] not in vertices) or ([afiliaciones_entry[j][0], afiliaciones_entry[i][0]] not in vertices)):
                            vertices += [[afiliaciones_entry[i][0], afiliaciones_entry[j][0]]]
            contador += 1
            #print(afiliaciones_entry)
            #print('SIGUIENTE')


        #print('Fin')


print(obtener_metadatos(archivoxml, '{http://www.w3.org/2005/Atom}affiliation', mis_nodos, mis_vertices))
print('Mis vertices:', len(mis_vertices), mis_vertices)
print('Mis Nodos:', len(mis_nodos), mis_nodos)

mis_nodos_coord = hacerlista_desdexml(mis_nodos, 20)

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

desc_nodos(mis_nodos_coord, mis_vertices_coord, latsmpl, lonsmpl, nomsmpl, vertsmpl)

mplmap(lonsmpl, latsmpl, nomsmpl, vertsmpl, 1)

path = os.path.abspath('jajajaja.txt')
f = open(path, 'w')
f.write(str(vertsmpl))