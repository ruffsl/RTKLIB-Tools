'''
Created on Jul 26, 2013

@author: ruffin
'''
import os, sys
import shutil
import subprocess
import locale
from ftplib import FTP
from ephem_utils import *
from file_utils import *
from gpstime import *

from pandas.lib import Timestamp
import pandas as pd
import numpy as np
import geopy as gp
from geopy import distance



#------------------------------------------------------------------------------ 
# Convert ubx files
#------------------------------------------------------------------------------ 
def convbinFile(dir, file, convbin):
	os.chdir(dir)
	filename = os.path.splitext(file)[0]
	if (os.path.isdir(filename) == 0):
		os.mkdir(filename)
	#shutil.move(file, dir + filename)
	shutil.copyfile(file,dir + filename + '/' + file)
	os.chdir(dir + filename)
	command = ([convbin, dir + filename + '/' + file, '-v', '3.02', '-od', '-os', '-oi', '-ot', '-ol'])
	print('Running ')
	print(' '.join(command))
	subprocess.check_output(command)
	
#------------------------------------------------------------------------------ 
# Convert ubx files
#------------------------------------------------------------------------------ 
def rnx2rtkpFile(indir, filename, outdir, station, rnx2rtkp):
	#filename = os.path.splitext(file)[0]
	#filename = file
	os.chdir(indir + filename)
	obsfile = findFile(indir + filename,".obs")
	command = ['grep', 'TIME OF FIRST OBS', indir + filename + '/' + obsfile]
	ymdhms = subprocess.check_output(command).decode(locale.getdefaultlocale()[1])
	tdate = datetime.strptime(ymdhms[:42], ' %Y %m %d %H %M %S.%f')
	gpsweek = gpsWeek(tdate.year, tdate.month, tdate.day)
	gpsweekday = dayOfWeek(tdate.year, tdate.month, tdate.day)
	julianday = julianDay(tdate.year, tdate.month, tdate.day)
		
	sp3file = str(gpsweek) + str(gpsweekday) +'.sp3'
	
	os.chdir(indir)
	for file in os.listdir("."):
	    if file.endswith(sp3file):
	        sp3file = file
	    if file.endswith(sp3file):
	        sp3file = file
	    if file.endswith('rtkoptions_static.conf'):
	        staticConf = file
	    if file.endswith('rtkoptions_kinetic.conf'):
	        kineticConf = file
        
    
	navfilePath = indir + filename + '/' + filename + '.nav'
	obsfilePath = indir + filename + '/' + filename + '.obs'
	sbsfilePath = indir + filename + '/' + filename + '.sbs'
	o13filePath = indir + station + str(julianday) + '0.13o'
	sp3filePath = indir + sp3file
	staticConfPath  = indir + staticConf
	kineticConfPath = indir + kineticConf
	staticPosPath =  outdir + filename + '/' + filename + '_static.pos'
	kineticPosPath = outdir + filename + '/' + filename + '_kinetic.pos'
	
	if('.v' in filename):
		originalFile = filename.split('.v')[0]
		originalstaticPosPath =  outdir + originalFile + '/' + originalFile + '_static.pos'
		checkDir(staticPosPath[:-11],'w')
		shutil.copyfile(originalstaticPosPath, staticPosPath)
		print('Copy static from original')
	else:
		command0 = ([rnx2rtkp,'-k', staticConfPath,'-o', staticPosPath, obsfilePath, o13filePath, navfilePath, sp3filePath, sbsfilePath])
		print('\nRunning ')
		print(' '.join(command0))
		subprocess.check_output(command0)
	
	command1 = ([rnx2rtkp,'-k', kineticConfPath,'-o', kineticPosPath, obsfilePath, o13filePath, navfilePath, sp3filePath, sbsfilePath])
	print('\nRunning ')
	print(' '.join(command1))
	subprocess.check_output(command1)


#------------------------------------------------------------------------------ 
# Convert ubx files
#------------------------------------------------------------------------------ 
def fetchData(dir, file, server, hostPath, station):
	# Extract time stamp from log files
	filename = os.path.splitext(file)[0]
	os.chdir(dir + filename)
	obsfile = findFile(dir + filename,".obs")
	
	# Parsing time from data
	command = ['grep', 'TIME OF FIRST OBS', dir + filename + '/' + obsfile]
	#print('Running ')
	#print(' '.join(command))
	ymdhms = subprocess.check_output(command).decode(locale.getdefaultlocale()[1])
	tdate = datetime.strptime(ymdhms[:42], ' %Y %m %d %H %M %S.%f')
	tnow = datetime.now()
	#print('Recorded Date')
	#print(tdate, end='\n\n')
	#print('Current Date')
	#print(tnow, end='\n\n')
	dt = tnow - tdate
	#print('Date Diffrince')
	#print(dt, end='\n\n')
	
	# Get files from FTP server
	corfile = station + tdate.strftime("%j0.%y") + 'o.gz'
	navfile = station + tdate.strftime("%j0.%y") + 'd.Z'
	hostPath = hostPath + tdate.strftime("%Y/%j/")

	ftp = FTP(server)
	ftp.login()
	
	#print('Fetching updated ephemerides')
	if fetchFiles(ftp, hostPath, dir, 'igs*'):
		print('No IGS file yet')
		if fetchFiles(ftp, hostPath, dir, 'igr*'):
			print('No IGR file yet')
			if fetchFiles(ftp, hostPath, dir, 'igu*'):
				print('Not even an IGU file yet')
				print('Have a little patients!')
	hostPath = hostPath + station
	#print('FTP Current Working Directory\n' + hostPath, end='\n\n')
	#print('Fetching station broadcasts')
	if fetchFiles(ftp, hostPath, dir):
		print('No data files yet')

	ftp.quit()
	
def buildDataFrame(dir, folder):
	staticPosFile = findFile(dir + folder,'_static.pos')
	kineticPosFile = findFile(dir + folder,'_kinetic.pos')
	
	skiprow = 0
	with open(staticPosFile) as search:
		for i, line in enumerate(search):
			if "%  GPST" in line:
				skiprow = i
				break
	dff = pd.read_csv(staticPosFile, skiprows=skiprow, delim_whitespace=True, parse_dates=[[0, 1]])
	qmin = dff['Q'].min()
	print('qmin:', qmin)
	qmins = dff['Q'] == qmin
	print('qmins:',len(qmins))
	if (len(qmins) > 1):
		dff = dff[qmins]
	reference = gp.point.Point(dff['latitude(deg)'].mean(), dff['longitude(deg)'].mean(), dff['height(m)'].mean())
	print(reference.latitude, reference.longitude, reference.altitude)
	
	skiprow = 0
	with open(kineticPosFile) as search:
	    for i, line in enumerate(search):
	        if "%  GPST" in line:
	            skiprow = i
	            break
	df = pd.read_csv(kineticPosFile, skiprows=skiprow, delim_whitespace=True, parse_dates=[[0, 1]])
	#reference = gp.point.Point(df['latitude(deg)'][0], df['longitude(deg)'][0], df['height(m)'][0])
	
	df['sd(m)'] = np.sqrt(df['sdn(m)']**2+df['sde(m)']**2+df['sdu(m)']**2+df['sdne(m)']**2+df['sdeu(m)']**2+df['sdun(m)']**2)
	df['dist(m)'] = 0.0
	df['distn(m)'] = 0.0
	df['diste(m)'] = 0.0
	df['distu(m)'] = 0.0
	d = distance.distance
	for i in df.index :
	    j = gp.point.Point(df['latitude(deg)'][i],df['longitude(deg)'][i])
	    k = gp.point.Point(reference.latitude,df['longitude(deg)'][i])
	    l = gp.point.Point(df['latitude(deg)'][i],reference.longitude)
	    
	    lat1 = math.radians(reference.latitude)
	    lon1 = math.radians(reference.longitude)
	    lat2 = math.radians(df['latitude(deg)'][i])
	    lon2 = math.radians(df['longitude(deg)'][i])
	    
	    dLon = lon2 - lon1;
	    y = math.sin(dLon) * math.cos(lat2);
	    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon);
	    brng = math.atan2(y, x);
	    north = math.cos(brng)
	    east = math.sin(brng)
	    
	    j = d(reference, j).meters
	    k = d(reference, k).meters*np.sign(east)
	    l = d(reference, l).meters*np.sign(north)
	    m = (df['height(m)'][i] - reference.altitude)
	    q = np.core.sqrt(j**2+m**2)
	    
	    df['dist(m)'][i] = q
	    df['distn(m)'][i] = k
	    df['diste(m)'][i] = l
	    df['distu(m)'][i] = m
	return df
	

#------------------------------------------------------------------------------ 
# Decompress downloaded files
#------------------------------------------------------------------------------ 
def decompressData(dir):
	# print('Uncompressing fetched data')
	subprocess.check_output(['gzip', '-d', '-f', '-r', dir])
	
def readObs(dir, file):
    #Read header
    header = ''
    with open(dir + file) as handler:
        for i, line in enumerate(handler):
            header += line
            if 'END OF HEADER' in line:
                break
    #Read Data
    with open(dir + file) as handler:
        #Make a list to hold dictionaries
        date_list = []
        for line in handler:
            #Check for a Timestamp lable
            if '> ' in line:
            	#Grab Timestamp
                links = line.split()
                index = datetime.strptime(' '.join(links[1:7]), '%Y %m %d %H %M %S.%f0')
                #Identify number of satellites
                satNum = int(links[8])
                #For every sat
                for sat in range(satNum):
                    #Make a holder dictionary
                    sat_dict = {}
                	#just save the data as a string for now
                    satData = handler.readline()
                    #Fix the names
                    satID = satData.replace("G ", "G0").split()[0]
                    #Add holder dictionary
                    sat_dict['%_GPST'] = index
                    sat_dict['satID'] = satID
                    sat_dict['satData'] = satData
                    #Add to the growing list
                    date_list.append(sat_dict)
    #Convert to dataframe
    df = pd.DataFrame(date_list)
    #Set the multi index
    df = df.set_index(['%_GPST', 'satID'])
    return df, header
	
def writeObs(dir, file, df, header):
    #Write header
    with open(dir + file, 'w') as handler:
    	handler.write(header)	
    
    with open(dir + file, 'a') as handler:
        for group in df.groupby(level=0, axis=0):
            timestampObj = group[0]
            dff = group[1]
            sats = len(dff.index)
            timestampLine = timestampObj.strftime('> %Y %m %d %H %M %S.%f0  0 ') + str(sats) + '\n'
            handler.write(timestampLine)	
            for sat in range(sats):
                satDataLine = dff.ix[sat][0]
                handler.write(satDataLine)
    return 0
	
	
def getSatsList(df):
	df = df.reset_index()
	uniq_satID = df['satID'].unique()
	uniq_satID = [x[1:] for x in uniq_satID if not 'S' in x]
	return uniq_satID

def xyz2plh(x,y,z):
    emajor = 6378137.0
    eflat  = 0.00335281068118
    A = emajor 
    FL = eflat
    ZERO = 0.0
    ONE = 1.0
    TWO = 2.0
    THREE = 3.0
    FOUR = 4.0
    
    '''
    1.0 compute semi-minor axis and set sign to that of z in order
        to get sign of Phi correct
    '''
    B = A * (ONE - FL)
    if( z < ZERO ):
        B = -B
    '''
    2.0 compute intermediate values for latitude
    '''
    r = math.sqrt( x*x + y*y )
    e = ( B*z - (A*A - B*B) ) / ( A*r )
    f = ( B*z + (A*A - B*B) ) / ( A*r )
    
    '''
    3.0 find solution to:
        t^4 + 2*E*t^3 + 2*F*t - 1 = 0
    '''
    p = (FOUR / THREE) * (e*f + ONE)
    q = TWO * (e*e - f*f)
    d = p*p*p + q*q
    
    if( d >= ZERO ):
        v= pow( (sqrt( d ) - q), (ONE / THREE) ) - pow( (sqrt( d ) + q), (ONE / THREE) )
    else:
        v= TWO * sqrt( -p ) * cos( acos( q/(p * sqrt( -p )) ) / THREE )
    '''
    4.0 improve v
        NOTE: not really necessary unless point is near pole
    '''
    if( v*v < fabs(p) ):
        v = -(v*v*v + TWO*q) / (THREE*p)
    g = (sqrt( e*e + v ) + e) / TWO
    t = sqrt( g*g  + (f - v*g)/(TWO*g - e) ) - g
    
    lat = math.atan( (A*(ONE - t*t)) / (TWO*B*t) )
    
    '''
    5.0 compute height above ellipsoid
    '''
    elv = (r - A*t)*cos( lat ) + (z - B)*sin( lat );
    
    '''
    6.0 compute longitude east of Greenwich
    '''
    zlong = math.atan2( y, x )
    if( zlong < ZERO ):
        zlong = zlong + math.pi*2
    lon = zlong
    
    '''
    7.0 convert latitude and longitude to degrees
    '''
    lat = np.rad2deg(lat)
    lon = np.rad2deg(lon)
    lon = -math.fmod((360.0-lon), 360.0)
    
    return lat, lon, elv

def diff2Angles(firstAngle, secondAngle):
    difference = secondAngle - firstAngle
    difference =  mod( secondAngle - firstAngle + 180, 360 ) - 180
    return difference

def generateMaskList(satConsts):
    satConsts = sorted(satConsts, key=lambda tup: tup[2])
    angels = []
    for i in range(len(satConsts)):
        a = np.deg2rad(satConsts[i-1][2])
        b = np.deg2rad(satConsts[i][2])
        c = math.atan2((sin(a)+sin(b)),(cos(a)+cos(b)))
        c = np.rad2deg(c)
        c = math.fmod((c+360), 360.0)
        angels.append(c)
    maskList = []
    for i, mask in enumerate(angels):
        masks = []
        for j, sat in enumerate(satConsts):
            diff = diff2Angles(sat[2],mask)
            if diff < 0:
                masks.append(sat[0])
        maskList.append(masks)
    return maskList

def applyMasks(df, satConsts):
	dfs = []
	maskList = generateMaskList(satConsts)
	for mask in maskList:
		dff = df
		dff = dff.reset_index()
		print(mask)
		for sat in mask:
		    dff = dff[dff['satID'] != sat]
		dff = dff.set_index(['%_GPST', 'satID'])
		dfs.append(dff)
	return dfs

def generateData(dir, noradFile):
    folders = findFolders(dir)
    for folder in folders:
        print('reading: ' + dir + folder + '/' + folder + '.obs')
        df, header = readObs(dir + folder + '/', folder + '.obs')
        headerLines = header.split('\n')
        for line in headerLines:
            if 'APPROX POSITION XYZ' in line:
                list = line.split()
                x = float(list[0])
                y = float(list[1])
                z = float(list[2])
                lat, lon, elv = xyz2plh(x,y,z)
                break
        lat, lon, elv = xyz2plh(x,y,z)
        reference = gp.point.Point(lat,lon,elv)
        date = df.index[0][0]
        satlist = loadTLE(dir + noradFile)
        satObs = getSatsList(df)
        satConsts = getSatConsts(satlist, satObs, date, reference)
        dfs = applyMasks(df, satConsts)
        
        for x, dfx in enumerate(dfs):
            folderx = folder + '.v' + str(x)
            dirx = dir + folderx + '/'
            filepathx = dirx + folderx	
            filepath = dir + folder + '/' + folder
            checkDir(dirx,'w')
            writeObs(dirx, folderx + '.obs', dfx, header)
            shutil.copyfile(filepath + '.nav', filepathx + '.nav')
            shutil.copyfile(filepath + '.sbs', filepathx + '.sbs')
