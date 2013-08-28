'''
Created on Aug 2, 2013

@author: ruffin
'''
import pandas as pd
import scipy as sp
import numpy as np
import geopy as gp
import ephem
import urllib.request
import shutil
from Utils.file_utils import *

def loadTLE(filename):
    """ Loads a TLE file and creates a list of satellites."""
    f = open(filename)
    satlist = []
    l1 = f.readline()
    while l1:
        l1 = [s[:-1] for s in l1.split() if s[:-1].isdigit()][0]
        l2 = f.readline()
        l3 = f.readline()
        sat = ephem.readtle(l1,l2,l3)
        satlist.append(sat)
        l1 = f.readline()

    f.close()
    #print("%i satellites loaded into list"%len(satlist))
    return(satlist)

def getSatConsts(satlist, satObs, date, reference):
    constellations = []
    for sat in satlist:
        if sat.name in satObs:
            #print(sat.name)
            constellation = getSatConst(sat, date, reference)
            constellations.append(constellation)
    return(constellations)

def getSatConst(sat, date, reference):
    observer = ephem.Observer()
    observer.lat = np.deg2rad(reference.latitude)
    observer.long = np.deg2rad(reference.longitude)
    observer.date = date
    sat.compute(observer)
    sat_alt = np.rad2deg(sat.alt)
    sat_az  = np.rad2deg(sat.az)
    constellation = ['G' + sat.name, sat_alt, sat_az]
    return(constellation)