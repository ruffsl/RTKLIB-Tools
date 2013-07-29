'''
Created on Jul 1, 2013

@author: ruffin
'''

import os
from pylab import *
from datetime import *
import numpy as np
import ftplib
from ftplib import FTP

def checkDir(dir,option):
    """Check Directory""" 
    if not dir.endswith('/'):
        dir += '/'
    if option == 'w':
        if not os.path.exists(dir):
            os.makedirs(dir)
    print('Checking directory: ' + dir)
    return dir
    
def findFile(dir,extension):
    file = 0
    os.chdir(dir)
    for files in os.listdir("."):
        if files.endswith(extension):
            file = files
    return file

def findFiles(dir,extension):
    os.chdir(dir)
    allFiles = os.listdir(".")
    foundFiles = []
    for file in allFiles:
        if file.endswith(extension):
            foundFiles.append(file)
    return foundFiles


def parsePosFile(posFile):
    """Parses pos file for data"""
    print('Parsing file: ' + posFile)
    data = np.zeros([1,14])
    with open(posFile, 'r') as f:
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

def fetchFiles(ftp, path, dir, key=None):
    try:
        ftp.cwd(path)
        os.chdir(dir)
        if key == None:
            list = ftp.nlst()
        else:
            list = ftp.nlst(key)
        for filename in list:
            haveFile =False
            for file in os.listdir("."):
                if file in filename:
                    haveFile = True
            if haveFile:
                print('Found local\n' + filename, end = '\n\n')
            else:
                print('Downloading\n' + filename, end = '\n\n')
                fhandle = open(os.path.join(dir, filename), 'wb')
                ftp.retrbinary('RETR ' + filename, fhandle.write)
                fhandle.close()
        return False
    except ftplib.error_perm:
        return True
