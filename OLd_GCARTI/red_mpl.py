

def desc_nodos(nodos, vertices, lats, lons, noms):#, verti): # lats, lons, noms son listas vacias. # verts es un str vacio

    for i in nodos:
        lats += [i[4]]
        lons += [i[5]]
        noms += [i[0]]
    verti=''

    for i in vertices:
        verti += """x1,y1=my_map("""+str([i[0][1], i[1][1]])+""", """+str([i[0][0], i[1][0]])+""")
         my_map.plot(x1, y1, linewidth=1, color='k', markerfacecolor='b')
         """

    return verti


