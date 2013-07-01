'''
Created on Jun 26, 2013

@author: ruffin
'''
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
k = point.Point(40.442635758, -79.943065017)
# k = Point(40.443874, -79.945517)


#------------------------------------------------------------------------------ 
# Check output directory can be dumped to
#------------------------------------------------------------------------------ 
indir = checkDir(indir,'r')
outdir = checkDir(outdir,'w')

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
 
# Show result on screen
lp.show()