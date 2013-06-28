'''
Created on Jun 26, 2013

@author: ruffin
'''
if __name__ == '__main__':
    pass
import os
from pylab import *
from datetime import *
import numpy as np
# import geopy as gp
from geopy import geocoders , point
from geopy import distance
from geopy.point import Point


# str = input("Enter your input: ");
# print("Received input is : ", str)

#------------------------------------------------------------------------------ 
# File Directory
#------------------------------------------------------------------------------ 
indir = '/home/ruffin/Documents/Data/in/'
outdir = '/home/ruffin/Documents/Data/out/'
# k = Point(40.442635758, -79.943065017)
k = Point(40.443874, -79.945517)


#------------------------------------------------------------------------------ 
# Check output directory can be dumped to
#------------------------------------------------------------------------------ 
if not outdir.endswith('/'):
    outdir += '/'
if not os.path.exists(outdir):
    os.makedirs(outdir)
    

#------------------------------------------------------------------------------ 
# Get log gps file name
#------------------------------------------------------------------------------ 
os.chdir(outdir)
for file in os.listdir("."):
    if file.endswith(".pos"):
        obsfile = file
        namefile = obsfile
print('File name base found to be: ' + namefile, end='\n')

data = np.zeros([1,14])

with open(obsfile, 'r') as f:
#     read_data = f.read()
    for line in f:
        if(line[0]!='%'):
#             print(line, end='\n')
            tdate = datetime.strptime(line[:23], '%Y/%m/%d %H:%M:%S.%f')
            tdate = datetime.timestamp(tdate)
            lon = float(line[25:38])
            lat = float(line[40:53])
            elv = float(line[55:64])
            q = int(line[66:68])
            ns = int(line[70:72])
            sdn = float(line[74:81])
            sde = float(line[83:90])
            sdu = float(line[92:99])
            sdne = float(line[101:108])
            sdeu = float(line[110:117])
            sdun = float(line[119:126])
            age =  float(line[127:133])
            ratio = float(line[135:])
            temp = np.array([tdate, lon, lat, elv, q, ns, sdn, sde, sdu, sdne, sdeu, sdun, age, ratio])
            data = vstack((data, temp))
f.closed

# data = list((zip(*data)))
# data.transpose()
data = np.delete(data, 0, 0)
data = data.T
 
# Create a new figure of size 8x6 points, using 80 dots per inch
# figure(figsize=(8,6), dpi=80)
figure(figsize=(10,6), dpi=80)
 
# Create a new subplot from a grid of 1x1
subplot(1,1,1)
 
# X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
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

plot(tdate,sdn, label='sdn')
plot(tdate,sde, label='sde')
plot(tdate,sdu, label='sdu')
plot(tdate,sdne, label='sdne')
plot(tdate,sdeu, label='sdeu')
plot(tdate,sdun, label='sdun')

dist = np.array([])
d = distance.distance
for i in data.T:
    j = Point(i[1],i[2])
    dist = np.append(dist, [d(k, j).meters], axis=0)
# print(dist)
plot(tdate,dist, label='dist')

# print(lon[0],lat[0])

legend(loc='upper left')

# Save figure using 72 dots per inch
# savefig("exercice_2.png",dpi=72)
 
# Show result on screen
show()