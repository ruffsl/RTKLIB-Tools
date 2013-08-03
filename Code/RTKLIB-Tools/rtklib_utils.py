'''
Created on Jul 26, 2013

@author: ruffin
'''
import os, sys
import shutil
import subprocess
import locale
from ftplib import FTP
from file_utils import *
from gpstime import *

from pandas.lib import Timestamp
import pandas as pd
import numpy as np
import geopy as gp




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
def rnx2rtkpFile(indir, file, outdir, station, rnx2rtkp):
	filename = os.path.splitext(file)[0]
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
	
	command0 = ([rnx2rtkp,'-k', staticConfPath,'-o', staticPosPath, obsfilePath, o13filePath, navfilePath, sp3filePath, sbsfilePath])
	print('\nRunning ')
	print(' '.join(command0))
	subprocess.check_output(command0)
	command1 = ([rnx2rtkp,'-k', kineticConfPath,'-o', kineticPosPath, obsfilePath, o13filePath, navfilePath, sp3filePath, sbsfilePath])
	print('\nRunning ')
	print(' '.join(command1))
	subprocess.check_output(command1)
	
# 	os.chdir(indir)
# 	filename = os.path.splitext(file)[0]
# 	if (os.path.isdir(filename) == 0):
# 		os.mkdir(filename)
# 	#shutil.move(file, dir + filename)
# 	shutil.copyfile(file,dir + filename + '/' + file)
# 	os.chdir(dir + filename)
# 	command = ([convbin, dir + filename + '/' + file])
# 	print('Running ')
# 	print(' '.join(command))
# 	subprocess.check_output(command)


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
	staticPosFile = findFile(dir + folder,'static.pos')
	kineticPosFile = findFile(dir + folder,'kinetic.pos')
	
	skiprow = 0
	with open(staticPosFile) as search:
		for i, line in enumerate(search):
			if "%  GPST" in line:
				skiprow = i
				break
	dff = pd.read_csv(kineticPosFile, skiprows=skiprow, delim_whitespace=True, parse_dates=[[0, 1]])
	qmin = dff['Q'].min()
	print('qmin:', qmin)
	qmins = dff['Q'] == qmin
	print('qmins:',len(qmins))
	if (len(qmins) > 1):
		dff = dff[qmins]
	reference = gp.point.Point(dff['latitude(deg)'].mean(), dff['longitude(deg)'].mean(), dff['height(m)'].mean())
	print(folder)
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
	d = gp.distance.distance
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
	
def genData(dir, file):
	dfObs, headerObs = readObs(dir, file)
	satObs = dfObs['satID'].unique()
	satObs = [x for x in satObs if not 'S' in x]
	
	satlistObs = foo
	for i in satlistObs:
		if 


def readObs(dir, file):
    df = pd.DataFrame()
    #Grab header
    header = ''
    with open(dir + file) as handler:
        for i, line in enumerate(handler):
            header += line
            if 'END OF HEADER' in line:
                break
    #Grab Data
    with open(dir + file) as handler:
        for i, line in enumerate(handler):
        	#Check for a Timestamp lable
            if '> ' in line:
            	#Grab Timestamp
                links = line.split()
                index = datetime.strptime(' '.join(links[1:7]), '%Y %m %d %H %M %S.%f0')
                #Identify number of satellites
                satNum = int(links[8])
                #For every sat
                for j in range(satNum):
                	#just save the data as a string for now
                    satData = handler.readline()
                    #Fix the names
                    satdId = satData.replace("G ", "G0").split()[0]
                    #Make a dummy dataframe
                    dff = pd.DataFrame([[index,satdId,satData]], columns=['%_GPST','satID','satData'])
                    #Tack it on the end
                    df = df.append(dff)
    return df, header
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	