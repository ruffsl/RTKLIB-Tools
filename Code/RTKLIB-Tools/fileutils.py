'''
Created on Jul 1, 2013

@author: ruffin
'''

import os
from pylab import *
from datetime import *
import numpy as np

def checkDir(dir,option):
    """Check Directory""" 
    if not dir.endswith('/'):
        dir += '/'
    if option == 'w':
        if not os.path.exists(dir):
            os.makedirs(dir)
    return dir
    
def findFile(dir,extension):
    file = 0
    os.chdir(dir)
    for files in os.listdir("."):
        if files.endswith(extension):
            file = files
    print('File name base found to be: ' + file, end='\n\n')
    return file

def parseObsFile(obsFile):
    """Parses obs file for data"""
    data = np.zeros([1,14])
    with open(obsFile, 'r') as f:
        for line in f:
            if(line[0]!='%'):
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
    return data