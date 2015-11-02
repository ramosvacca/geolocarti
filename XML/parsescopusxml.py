__author__ = 'RAMOSVACCA'

#from xml.etree import cElementTree as ET
import xml.etree.ElementTree as ET

f=open('/Volumes/Ramosvacca/Github/geolocarti/XML/Scopus_geolocation.xml')
rr=f.read()
#print(rr)

"""nodos = []
vertices = []
articulos  = []

def esnumero(lista, entra):
    try:
        lista.index(entra)
        #int(entra)
        return True
    except ValueError:
        return False

#while (esnumero(rr.index("<entry>"))==True):

while (esnumero(rr, '<entry>')==True):
    articulos = articulos + rr.split("</entry>", 1)
    rr = rr[rr.index('</entry>'):]

rr = rr[rr.index('</entry>'):]
print(rr)"""

def obtener_metadatos(xml, campos):
        respuesta = []
        tree = ET.parse(xml)
        root = tree.getroot()
        for child in root:
            for campito in child:
                for campo in campos:
                    #print campito.tag
                    if campito.tag == campo:
                        #print campito.text, campito.tag
                        respuesta.append(campito.text)
        return respuesta

obtener_metadatos(rr, 'affiliation')




