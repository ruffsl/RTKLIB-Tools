'''
Created on Jun 26, 2013

@author: ruffin
'''

if __name__ == '__main__':
    pass
# from pylab import *
from matplotlib import pyplot, mpl
import numpy as np
from geopy import point, distance
from plot_utils import *
from file_utils import *

# str = input("Enter your input: ");
# print("Received input is : ", str)

#------------------------------------------------------------------------------ 
# File Directory
#------------------------------------------------------------------------------ 
indir = '/home/ruffin/Documents/Data/in/'
outdir = '/home/ruffin/Documents/Data/out/'
# reference = point.Point(40.442635758, -79.943065017, 257)
reference = point.Point(40.443874, -79.945517, 272)

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
data = parsePosFile(posFile)


#------------------------------------------------------------------------------ 
# Parse data from log file
#------------------------------------------------------------------------------ 
print('Interpolating Data')
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
distn = np.array([])
diste = np.array([])
distu = np.array([])
distne = np.array([])
disteu = np.array([])
distun = np.array([])
d = distance.distance
for i in data.T:
    j = point.Point(i[1],i[2])
    k = point.Point(reference.latitude,i[2])
    l = point.Point(i[1],reference.longitude)
    
    j = d(reference, j).meters
    k = d(reference, k).meters*np.sign(i[1]-reference.latitude)
    l = d(reference, l).meters*np.sign(i[2]-reference.longitude)
    m = (i[3] - reference.altitude)
    
    n = np.core.sqrt(k**2+l**2)*np.sign(k)
    o = np.core.sqrt(l**2+m**2)*np.sign(l)
    p = np.core.sqrt(m**2+k**2)*np.sign(m)
    
    dist = np.append(dist, [j], axis=0)
    distn = np.append(distn, [k], axis=0)
    diste = np.append(diste, [l], axis=0)
    distu = np.append(distu, [m], axis=0)
    distne = np.append(distne, [n], axis=0)
    disteu = np.append(disteu, [o], axis=0)
    distun = np.append(distun, [p], axis=0)

sd = ['sdn','sde','sdu','sdne','sdeu','sdun']
sdd = ['distn','diste','distu','distne','disteu','distun']
sddist = [distn,diste,distu,distne,disteu,distun]

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

distnmin = distn.min()
distnmax = distn.max()
distemin = diste.min()
distemax = diste.max()

distndif = distnmax - distnmin
distedif = distemax - distemin

distnminlim = distn.min() - distndif*0.1
distnmaxlim = distn.max() + distndif*0.1
disteminlim = diste.min() - distedif*0.1
distemaxlim = diste.max() + distedif*0.1

distmax = dist.max()
distmin = dist.min()
distnorm = mpl.colors.Normalize(vmin=-distmax, vmax=0)

#------------------------------------------------------------------------------ 
# Plot data
#------------------------------------------------------------------------------ 
print('Generating Fig 1')
# Create a new figure of size 10x6 points, using 80 dots per inch
fig1 = pyplot.figure(figsize=(10,6), dpi=80)
fig1.suptitle('Dist and Standard Deviation vs Time', fontsize=14, fontweight='bold')
ax = fig1.add_subplot(1,1,1)
  
# Make plots
for i in range(6):
    sdx = data[i+6]
    ax.plot(tdate, sdx, label=sd[i])

ax.plot(tdate,dist, label='dist')
ax.grid(True)
ax.set_ylabel('Meters')
ax.set_xlabel('Seconds')
  
# Make legend
pyplot.legend(loc='upper left')
  
# Save figure using 72 dots per inch
# pyplot.savefig("exercice_2.png",dpi=72)

 
print('Generating Fig 2')
fig2 = pyplot.figure(figsize=(10,6), dpi=80)
fig2.suptitle('Correlation of Standard Distribution vs Distance', fontsize=14, fontweight='bold')

for i in range(6):
    sdx = data[i+6]
    color = -np.core.sqrt(sdx**2+sddist[i]**2)
    ax = fig2.add_subplot(2,3,i+1)
    ax.scatter(sdx,sddist[i], c=color, alpha=.2)
    ax.set_title(sd[i]+' vs ' +sdd[i])
    ax.set_ylabel(sdd[i]+' (m)')
    ax.set_xlabel(sd[i]+' (m)')
    ax.grid(True)
    print('Cross-correlation: ' + sd[i]+' vs ' +sdd[i])
    print(np.correlate(sdx, sddist[i]))
 
# # Show result on screen
# pyplot.show()



print('Generating Fig 3')
fig3 = pyplot.figure(figsize=(10,6), dpi=80)
fig3.suptitle('Position and Standard Distribution', fontsize=14, fontweight='bold')

sd = ['sdn','sde','sdu','sdne','sdeu','sdun']

for i in range(6):
    sdx = data[i+6]
    ax = fig3.add_subplot(2, 3, i+1)
    p = ax.scatter(distn, diste, c=-abs(sdx), alpha=.2)
    fig3.colorbar(p,norm=distnorm)    
    xlim(distnminlim, distnmaxlim)
    ylim(disteminlim, distemaxlim)    
    ax.set_title('Pos w/ ' + sd[i]) 
    ax.set_ylabel('North')
    ax.set_xlabel('East')
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


# Show result on screen

print('Generating Fig 4')
fig4 = pyplot.figure(figsize=(10,6), dpi=80)
fig4.suptitle('Position and Standard Distribution', fontsize=14, fontweight='bold')
ax = fig4.add_subplot(1, 1, 1)
p = ax.scatter(distn,diste, c=-dist, alpha=.2)
fig4.colorbar(p, norm=distnorm)
xlim(distnminlim, distnmaxlim)
ylim(disteminlim, distemaxlim)
ax.set_xlabel('East (meters)')
ax.set_ylabel('North (meters)')
ax.grid(True)


pyplot.show()