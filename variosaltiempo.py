
from irenelmapa import irenelmapa
import os
import webbrowser
from getfrommaps import enbuscador, findapi, enelmapa
from ZZ_variasbonito import mplmap
from threading import Thread


"""def varios(algo, descrhtml):
    html=irenelmapa(algo, descrhtml)
    path = os.path.abspath('temp.html')
    url='file://'+path
    print(html)
    with open(path, 'w') as f
        f.write(html)
    webbrowser.open(url)"""


def hacerlista_otros(x):
        global descrip
        descrip=[]
        lista=[]
        nombres=[]
        for i in x:
                busqfin=str(i.replace(" ","+"))
                actual=enelmapa(busqfin)
                #actual=findapi(busqfin)
                #actual=enbuscador(busqfin)
                lista = lista + [[i]+actual]
                provi = '<div class="info_content"> <h3>'+i+'</h3> <p> descripción </p> </div>'
                descrip = descrip + [[provi]]

        #print(lista)
        #print(descrip)

        return [lista, str(descrip)]


import math



def hacerlista_desdexml(matriz, hilos):
    def auxiliar(submatriz, outdict, contando):
        for x in submatriz:
            print('Coord', submatriz.index(x), ' de ', len(submatriz))
            print('Contar', contando)
            contando += 1
            busqueda = x[0],x[1],x[2]

            busqfin = str(busqueda).replace("'","").replace(' ','+').replace('(','').replace(')','')
            actual = enelmapa(busqfin)

            outdict.append(x+actual)


    chunksize = int(math.ceil(len(matriz) / float(hilos)))
    threads = []
    outs = []
    contar = 0

    for i in range(hilos):
        t = Thread(
            target=auxiliar,
            args=(matriz[chunksize * i:chunksize * (i+1)],
                  outs, contar))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return outs


        #print(lista)
        #print(descrip)