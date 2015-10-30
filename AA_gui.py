#!/usr/bin/python
 
#from Tkinter import * #Note Tkinter for python 2.*, tkinter for python 3+
# if you are using Python 3, comment out the previous line
# and uncomment the following line
from tkinter import *
from tkinter.filedialog import askopenfilename
from variosaltiempo import hacerlista, varios
from ZZ_variasbonito import mplmap


root = Tk() ; root.withdraw()
paravarios = 0 # Una variable que al final tendrá una matriz con 1) Una matriz con ('nombre', lat, lon). 2) lista con descripciones para el javscript de irenelmapa
 
#Set display sizes
WINDOW_W = 500
WINDOW_H = 70
def createDisplay():

    global aaa, root
    
    global tka, mimagen
    # create the tk window - within which
    # everything else will be built.
    tka = Tk()

    #mimagen = PhotoImage(file="geolocarti.gif")

    w1 = Label(tka, text='Geolocarti',
               fg = "light green",
               bg = "dark green",
               font = "Helvetica 26 bold"
               )
    # w1.logo = logo
    w1.pack()
    #Add a canvas area ready for drawing on
    canvas = Canvas(tka, width=WINDOW_W, height=WINDOW_H)
    canvas.pack()
    #Add an exit button
    #canvas.create_image(0,0, anchor=NW, image=BitmapImage(file="geolocarti.xbm"), state=NORMAL)

    abrirarchivo = Button(tka, text='Click para seleccionar lista ("*.txt" en el formato establecido)', command =imprimirpls)
    abrirarchivo.pack()

    botongooglemaps = Button(tka, text="Google Maps", command=googlemaps)
    botongooglemaps.pack()

    botonmplmapconl = Button(tka, text="Mpl con líneas", command=matplotlibmapconlineas)
    botonmplmapconl.pack()

    botonmplmapsinl = Button(tka, text="Mpl sin líneas", command=matplotlibmapsinlineas)
    botonmplmapsinl.pack()

    btn = Button(tka, text="Exit", command=terminate)
    btn.pack()

    tka.lift()

    # Start the tk main-loop (tis updates the tk display)
    tka.mainloop()



def terminate():
    global tka
    tka.destroy()
    exit()
 
def main():
    createDisplay()

def imprimirpls():
    global paravarios, lonsglobal, latsglobal, nomsglobal
    lonsglobal=[]
    latsglobal=[]
    nomsglobal=[]
    filename = askopenfilename(parent=root)
    print(filename)
    f=open(filename)
    rr=f.read()
    listic=rr.split('\n')
    print(listic)
    #print(listic)
    paravarios=hacerlista(listic)
    #print(paravarios[0])
    nuevalista = paravarios[0]
    print(nuevalista)
    for i in nuevalista:
        print(i)
    for i in nuevalista:
        lonsglobal=lonsglobal+[i[2]]
        latsglobal=latsglobal+[i[1]]
        nomsglobal=nomsglobal+[i[0]]
    print(lonsglobal)

def matplotlibmapconlineas():
    mplmap(lonsglobal, latsglobal, nomsglobal, 1)

def matplotlibmapsinlineas():
    mplmap(lonsglobal, latsglobal, nomsglobal, 0)

def googlemaps():
    varios(paravarios[0], paravarios[1])

if __name__ == '__main__':
    main()
