'''
Created on Jun 26, 2013

@author: ruffin
'''
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import normalize
from numpy.ma.core import sqrt
from matplotlib.colorbar import Colorbar
if __name__ == '__main__':
    pass
# from pylab import *
import pylab as lp
import numpy as np
from geopy import point, distance

from fileutils import *

# str = input("Enter your input: ");
# print("Received input is : ", str)

#------------------------------------------------------------------------------ 
# File Directory
#------------------------------------------------------------------------------ 
indir = '/home/ruffin/Documents/Data/in/'
outdir = '/home/ruffin/Documents/Data/out/'
# k = point.Point(40.442635758, -79.943065017)
k = point.Point(40.443874, -79.945517)


#------------------------------------------------------------------------------ 
# Check output directory can be dumped to
#------------------------------------------------------------------------------ 
indir = checkDir(indir,'r')
outdir = checkDir(outdir,'r')

#------------------------------------------------------------------------------ 
# Get log gps file name
#------------------------------------------------------------------------------ 
posFile = findFile(outdir,'.pos')

#------------------------------------------------------------------------------ 
# Parse data from log file
#------------------------------------------------------------------------------ 
data = parseObsFile(posFile)

data = np.delete(data, 0, 0)
data = data.T
tdate = data[0]-data[0][0]
lon = data[1]
lat = data[2]
elv = data[3]
q = data[4]
ns = data[5]
sdn = data[6]
sde = data[7]
sdu = data[8]
sdne = data[9]
sdeu = data[10]
sdun = data[11]
age = data[12]
ratio = data[13]
dist = np.array([])
d = distance.distance
for i in data.T:
    j = point.Point(i[1],i[2])
    dist = np.append(dist, [d(k, j).meters], axis=0)


#------------------------------------------------------------------------------ 
# Plot data
#------------------------------------------------------------------------------ 
# Create a new figure of size 10x6 points, using 80 dots per inch
lp.figure(figsize=(10,6), dpi=80)
  
# Create a new subplot from a grid of 1x1
lp.subplot(1,1,1)
  
# Make plots
lp.plot(tdate,sdn, label='sdn')
lp.plot(tdate,sde, label='sde')
lp.plot(tdate,sdu, label='sdu')
lp.plot(tdate,sdne, label='sdne')
lp.plot(tdate,sdeu, label='sdeu')
lp.plot(tdate,sdun, label='sdun')
lp.plot(tdate,dist, label='dist')
  
# Make legend
lp.legend(loc='upper left')
  
# Save figure using 72 dots per inch
# lp.savefig("exercice_2.png",dpi=72)
   
# # Show result on screen
# lp.show()

distmax = dist.max()
distmin = dist.min()
print(distmax)
print(distmin)

 
fig2 = lp.figure(figsize=(10,6), dpi=80)
fig2.suptitle('Correlation of Standard Distribution vs Distance', fontsize=14, fontweight='bold')
 
sd = ['sdn','sde','sdu','sdne','sdeu','sdun']
for i in range(6):
    sdx = data[i+6]
    color = -sqrt(sdx**2+dist**2)
    ax = fig2.add_subplot(2,3,i+1)
    ax.scatter(sdx,dist, c=color, alpha=.2)
    ax.set_title(sd[i]+' vs dist')
    ax.set_ylabel('dist (m)')
    ax.set_xlabel(sd[i]+' (m)')
    ax.grid(True)
 
# # Show result on screen
# lp.show()

color = colors()
latmin = lat.min()
latmax = lat.max()
lonmin = lon.min()
lonmax = lon.max()

latdif = latmax - latmin
londif = lonmax - lonmin

latminlim = lat.min() - latdif*0.1
latmaxlim = lat.max() + latdif*0.1
lonminlim = lon.min() - londif*0.1
lonmaxlim = lon.max() + londif*0.1


fig3 = lp.figure(figsize=(10,6), dpi=80)
fig3.suptitle('Position and Standard Distribution', fontsize=14, fontweight='bold')

sd = ['sdn','sde','sdu','sdne','sdeu','sdun']

for i in range(6):
    sdx = data[i+6]
    ax = fig3.add_subplot(2, 3, i+1)
    p = ax.scatter(lat,lon, c=-sdx, alpha=.2)
    fig3.colorbar(p)
    xlim(latminlim, latmaxlim)
    ylim(lonminlim, lonmaxlim)    
    ax.set_title('Pos w/ ' + sd[i])
    ax.set_xlabel('lat (deg)')
    ax.set_ylabel('lon (deg)')
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.grid(True)

# 3D stuff
# for i in range(1):
#     sdx = data[i+6]
#     ax = fig3.add_subplot(1, 1, i+1, projection='3d')
#     
#     ax.scatter(lat,lon, sdx, c=dist, edgecolors = 'none')
#     xlim(latminlim, latmaxlim)
#     ylim(lonminlim, lonmaxlim)
#     ax.set_title('Pos w/ ' + sd[i])
#     ax.set_xlabel('lat (deg)')
#     ax.set_ylabel('lon (deg)')
#     ax.set_ylabel(sd[i] +' (m)')


# lp.subplot(2,3,1)
# scatter(lat,lon, c=sdn, edgecolors = 'none')
# xlim(latminlim, latmaxlim)
# ylim(lonminlim, lonmaxlim)
# lp.subplot(2,3,2)
# scatter(lat,lon, c=sde, edgecolors = 'none')
# xlim(latminlim, latmaxlim)
# ylim(lonminlim, lonmaxlim)
# lp.subplot(2,3,3)
# scatter(lat,lon, c=sdu, edgecolors = 'none')
# xlim(latminlim, latmaxlim)
# ylim(lonminlim, lonmaxlim)
# lp.subplot(2,3,4)
# scatter(lat,lon, c=sdne, edgecolors = 'none')
# xlim(latminlim, latmaxlim)
# ylim(lonminlim, lonmaxlim)
# lp.subplot(2,3,5)
# scatter(lat,lon, c=sdeu, edgecolors = 'none')
# xlim(latminlim, latmaxlim)
# ylim(lonminlim, lonmaxlim)
# lp.subplot(2,3,6)
# scatter(lat,lon, c=sdun, edgecolors = 'none')
# xlim(latminlim, latmaxlim)
# ylim(lonminlim, lonmaxlim)

# Show result on screen

fig4 = lp.figure(figsize=(10,6), dpi=80)
fig4.suptitle('Position and Standard Distribution', fontsize=14, fontweight='bold')

sd = ['sdn','sde','sdu','sdne','sdeu','sdun']

ax = fig4.add_subplot(1, 1, 1)
cm = lp.cm.get_cmap('RdYlBu')
p = ax.scatter(lat,lon, c=-dist, alpha=.2)
fig4.colorbar(p)
xlim(latminlim, latmaxlim)
ylim(lonminlim, lonmaxlim)    
ax.set_title('Pos w/ ' + sd[i])
ax.set_xlabel('lat (deg)')
ax.set_ylabel('lon (deg)')
ax.grid(True)


# lp.colorbar(ax, cmap=dist, orientation='horizontal')
# cbar = ax.add_colorbar(dist, orientation='horizontal')
# cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])# horizontal colorbar


lp.show()