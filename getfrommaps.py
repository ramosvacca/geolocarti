# Para extraer la latitud y longitud de caulquier sitio, pasando por google maps

from mpl_toolkits.basemap import Basemap
import urllib.request
from regex import regcoord

#busqfin=str(input("Ingrese el nombre del sitio que desea buscar.")).replace(" ","+")#El nombre se ingresa normal, como str
#busqfin=busq.replace(' ','+') Buscar encoder URL.
#API_Key='dd'

## PARA EL API ##


def findapi(busqfin): #Es para encontrar las coordenadas de un sitio, con el nombre, mediante el api
    print('Inicia API')
    url_API_MapsGoogle='http://maps.google.com.co/maps/api/geocode/xml?address='+busqfin+'&sensor=false'

    req = urllib.request.Request(url_API_MapsGoogle)#la clave como variable Geocoding
    print(url_API_MapsGoogle)#Mejor pasar las direcciones como variables
    with urllib.request.urlopen(req) as response:
        a = str(response.read())
    try:
        b = a[a.index('lat')+4:a.index('/lat')-1]
        c = a[a.index('lng')+4:a.index('/lng')-1]
        name = a[a.index('long_name')+10:a.index('/long_name')-1]
        latlon = b, c
        print('El nombre es:', name, '\nLatitud y longitud -->', latlon)
        print(float(b), float(c))
        #latlon=[float(b), float(c)]
        latlon=(b,c)
        return(latlon)
    except ValueError:
        print('Api no encontró resultados')


#findgeopornombre()

## DESDE LA PÁGINA DE GOOGLE MAPS ##

from urllib.request import FancyURLopener
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def enelmapa(busqfin):
    print('Inicia fancito')
    myopener = MyOpener()
    page = myopener.open('https://www.google.com/maps?q='+busqfin)
    print('https://www.google.com/maps?q='+busqfin)
    prueba=page.read()
    a=str(prueba)
    #print(a)

    a=a[a.find('[[['):a.find('[[[')+150]
    b=a[a.find(',')+1:len(a)]
    lon=b[0:b.find(',')]
    lat=b[b.find(',')+1:b.find(']')]

    print('latlon ', lat, lon)
    
    latlon=[float(lat), float(lon)]
    print(latlon)
    return latlon

## DESDE GOOGLE SEARCH

import json

def enbuscador(algo):

    myopener=MyOpener()
    response = myopener.open('https://www.google.com.co/search?q='+algo)
    print('https://www.google.com.co/search?q='+algo)
    html = response.read()
    coords = regcoord(str(html))

    # req = urllib.request.Request('https://www.google.com.co/search?q='+algo)
    # with urllib.request.urlopen(req) as response:
    #     the_page = response.read()
    #
    # print(the_page)
    # coords = regcoord(str(the_page))
    print(html)
    print(coords)
    raw=coords[0]
    print(raw)
    lat=raw[0:raw.find(',')]
    print(lat)
    lon=raw[raw.find(',')+1:len(raw)]
    print(lon)
    lon=float(lon)
    lat=float(lat)
    latlon = [lat, lon]
    print(latlon)
    return latlon

    # url = 'https://www.google.com.co/search?q='+algo
    # r = urllib.request.urlopen(url)
    # data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    # print (data)

#print(enbuscador('Monash+Medical+School,+Monash+University,+Clayton,+VA+3800,+Australia'))
#enbuscador('Autonomous+university+of+the+occident,+cali,+colombia')
#enelmapa('Monash+Medical+School,+Monash+University,+Clayton,+VA+3800,+Australia')

