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





#------------------------------------------------------------------------------ 
# Convert ubx files
#------------------------------------------------------------------------------ 
def convbinFile(dir, file, convbin):
	os.chdir(dir)
	filename = os.path.splitext(file)[0]
	os.mkdir(filename)
	#shutil.move(file, dir + filename)
	shutil.copyfile(file,dir + filename + '/' + file)
	os.chdir(dir + filename)
	command = ([convbin, dir + filename + '/' + file])
	print('Running ')
	print(' '.join(command))
	subprocess.check_output(command)


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
		#print('No IGS file yet')
		if fetchFiles(ftp, hostPath, dir, 'igr*'):
			#print('No IGR file yet')
			if fetchFiles(ftp, hostPath, dir, 'igu*'):
				#print('Not even an IGU file yet')
				#print('Have a little patients!')
            
	hostPath = hostPath + station
	#print('FTP Current Working Directory\n' + hostPath, end='\n\n')
	#print('Fetching station broadcasts')
	if fetchFiles(ftp, hostPath, dir):
		print('No data files yet')

	ftp.quit()

