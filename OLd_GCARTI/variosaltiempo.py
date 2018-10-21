
from irenelmapa import irenelmapa
import os
import webbrowser
from getfrommaps import enbuscador, findapi, enelmapa
#from ZZ_variasbonito import mplmap
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

vigtech=['Instituto Nacional Cancerología, bogota', 'Center Cancer Research', 'International Conference MolecularTargets CancerTherapeutics', 'Organización Mundial Salud', 'Rev Colombiana Cancerología', 'Cancer Agency ORF', 'Internacional Agency Research Cancer', 'Centers Disease Control Prevention', 'National Cancer Institute', 'H&E Foundation Cancer Diagnosis', 'Action Against Cancer', 'National Cancer Institute', 'United States', 'Complementary Alternative Medicine Cancer', 'International Agency', 'DANE', 'SecretarÃía Distrital de Salud de Bogotá', 'Cancer Epidemiology Centre', 'European Journal Cancer', 'Ministerio de Salud bogota colombia', 'Ministerio de la Protección Social colombia', 'World Journal Gastroenterology', 'Universidad de Indiana', 'Journal Urol Clin North Am', 'Universidad Nacional de Colombia', 'Oxford University', 'Manizales Lab Bios', 'International Journal Cancer', 'Organización Panamericana de la Salud', 'Agencia Internacional para la Investigación', 'Universidad de Antioquia', 'Springer', 'Australian Institute', 'MedLine', 'Journal Clinical oncology', 'Grupo de Oncologí\xada Clí\xadnica', 'New England Journal Medicine', 'Fundación Santa Fe', 'Facultad de Medicina', 'EORTC Study Group', 'Imprenta Nacional', 'LILACS', 'Unidad de Cancer Hospital Villavicencio', 'Organización Europea para la Investigación', 'Departamento de Patologí\xada']

def hacerlista_desdexml(matriz, hilos):
    def auxiliar(submatriz, outdict, contando):
        for x in submatriz:
            print('Coord', submatriz.index(x), ' de ', len(submatriz))
            print('Contar', contando)
            contando += 1
            busqueda = x#[0]#,x[1],x[2]

            busqfin = str(busqueda).replace("'","").replace(' ','+').replace('(','').replace(')','')
            actual = enelmapa(busqfin)

            outdict.append([x, actual])#+actual)


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

print(hacerlista_desdexml(vigtech,4))

        #print(lista)
        #print(descrip)