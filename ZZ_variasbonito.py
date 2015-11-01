from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np

noms = ['Universidad del Valle', 'Massachussets Institute of Technology', 'Virginia Tech', 'Universidad del Norte']
lons = [-76.5, -71.06, -80.43, -74.8]
lats = [3.44, 42.43, 37.57, 10.99]

def mplmap(lons, lats, noms, a):
    a=1
##    my_map = Basemap(projection='lcc', lat_0 = -76.05, lon_0 = 21.55,
##        resolution = 'h', area_thresh = 0.1,
##        llcrnrlon= -4.3, llcrnrlat= -88.2,
##        urcrnrlon= 47.4, urcrnrlat= -63.9)

    my_map = Basemap(projection='merc', lat_0 = 21.55, lon_0 = -76.05,
        resolution = 'l', area_thresh = 1,
        llcrnrlon= -126, llcrnrlat= -4.3,
        urcrnrlon= -48, urcrnrlat= 51)
     
 #   my_map.drawcoastlines()
    my_map.drawcountries()
    # my_map.fillcontinents(color = 'coral', lake_color='aqua')
    # my_map.drawmapboundary(fill_color='aqua')
    if (a==1)==True:
        x1,y1=my_map([-76.5, -71.06], [3.44, 42.43])
        my_map.plot(x1, y1, linewidth=1, color='k', markerfacecolor='b')
        x1,y1=my_map([-76.5, -80.42], [3.44, 37.57])
        my_map.plot(x1, y1, linewidth=1, color='k', markerfacecolor='b')
        x1,y1=my_map([-76.5, -74.8], [3.44, 10.99])
        my_map.plot(x1, y1, linewidth=9, color='green', markerfacecolor='b')

    # lons = [-76.5, -71.06, -77.43, -74.8]
    # lats = [3.44, 42.43, 37.57, 10.99]
    x,y = my_map(lons, lats)
    my_map.plot(x, y, 'bo', markersize=10)
##
    #labels = ['Universidad del Valle', 'Massachussets Institute of Technology', 'Virginia Tech', 'Universidad del Norte']
    labels = noms
##    x_offsets = [-1000000, -700000, -50000, 3000]
##    y_offsets = [-280000, 200000, -300000, 150000]
    x_offsets = [200000,0,0,0]
    y_offsets = [81101,161110,161110,161110]

    for label, xpt, ypt, x_offset, y_offset in zip(labels, x, y, x_offsets, y_offsets):
        plt.text(xpt+x_offset, ypt+y_offset, label)
##

    my_map.shadedrelief()
    plt.show()

mplmap(lons,lats,noms,a=1)


