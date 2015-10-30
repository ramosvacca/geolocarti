from mpl_toolkits.basemap import Basemap 
import matplotlib.pyplot as plt 
import matplotlib.lines as lines 
import numpy as np 

m = Basemap(llcrnrlon=-11.5,llcrnrlat=51.0,urcrnrlon=-4.5,urcrnrlat=56.0, 
            resolution='i',projection='cass',lon_0=-4.36,lat_0=54.7) 

lats = [53.5519317,53.8758499, 54.2894659, 55.2333142, 
54.9846137,54.7064869, 51.5296651, 51.5536226, 51.7653115, 52.1625237, 
52.5809163, 52.9393892] 

lons = [-9.9413447, -9.9621948, -8.9583439, -7.6770179, -8.3771698, 
-8.7406732, -8.9529546, -9.7907148, -10.1531573, -10.4099873, 
-9.8456417, -9.4344939] 

x, y = m(lons, lats) # forgot this line 
m.plot(x, y, 'D-', markersize=10, linewidth=2, color='k', markerfacecolor='b') 
m.drawcoastlines() 
plt.show() 
