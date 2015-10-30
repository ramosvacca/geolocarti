
from irenelmapa import irenelmapa
import os
import webbrowser
from getfrommaps import enbuscador, findapi, enelmapa
from ZZ_variasbonito import mplmap



xy = ['El ombligo de Colombia, villavicencio',
'cano cristales, meta, colombia',
'Desierto de la Tatacoa, huila, colombia',
'san andres isla, colombia']

parabuscar = ['Universidad de los Andes, Bogota, Colombia',
     'Universidad del Valle, cali, colombia',
     'Universidad del Valle, zarzal, colombia',
     'Cideim, cali'
     ]




def varios(algo, descrhtml):

	html=irenelmapa(algo, descrhtml)
	path = os.path.abspath('temp.html')
	url='file://'+path
	print(html)

	with open(path, 'w') as f:
		f.write(html)
	webbrowser.open(url)

def hacerlista(x):
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
