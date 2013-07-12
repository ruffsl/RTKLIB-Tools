'''
Created on Jun 10, 2013

@author: whitemrj
'''
if __name__ == '__main__':
    pass

import subprocess
import os, sys
import locale
from datetime import datetime
from file_utils import *

encoding = locale.getdefaultlocale()[1]
#------------------------------------------------------------------------------ 
# File Directory
#------------------------------------------------------------------------------ 
indir = '/home/ruffin/Documents/Data/in/'
outdir = '/home/ruffin/Documents/Data/out/'
server = 'ftp.ngs.noaa.gov'
hostPath = '/cors/rinex/'
station = 'paap'
rnx2rtkp = '/home/ruffin/git/RTKLIB/app/rnx2rtkp/gcc/rnx2rtkp'
pos2kml  = '/home/ruffin/git/RTKLIB/app/pos2kml/gcc/pos2kml'
convbin  = '/home/ruffin/git/RTKLIB/app/convbin/gcc/convbin'
google_earth = '/usr/bin/google-earth'



#------------------------------------------------------------------------------ 
# Check output directory can be dumped to
#------------------------------------------------------------------------------ 
# print('Starting ublox script')
if not outdir.endswith('/'):
    outdir += '/'
if not os.path.exists(outdir):
    os.makedirs(outdir)

#------------------------------------------------------------------------------ 
# Convert log files
#------------------------------------------------------------------------------ 
# print('Checking ublox logs')
os.chdir(indir)
for file in os.listdir("."):
    if file.endswith(".ubx"):
        ubxfile = file
        namefile = os.path.splitext(ubxfile)[0]
print('File name base found to be:\n' + namefile, end='\n\n')

# print('Converting ublox logs')
command0 = ([convbin, namefile + '.ubx'])
print('Running ')
print(' '.join(command0))
subprocess.check_output(command0)


#------------------------------------------------------------------------------ 
# Extract time stamp from log files
#------------------------------------------------------------------------------ 
for file in os.listdir("."):
    if file.endswith(".obs"):
        obsfile = file

# print('Parsing time from data')
ymdhms = subprocess.check_output(['grep', 'TIME OF FIRST OBS', indir+obsfile]).decode(encoding)
tdate = datetime.strptime(ymdhms[:42], ' %Y %m %d %H %M %S.%f')
tnow = datetime.now()
print('Recorded Date')
print(tdate, end='\n\n')
print('Current Date')
print(tnow, end='\n\n')
dt = tnow - tdate
print('Date Diffrince')
print(dt, end='\n\n')

#------------------------------------------------------------------------------ 
# Get files from FTP server
#------------------------------------------------------------------------------
# print('Fetching NOAA CORS corrections') 
corfile = station + tdate.strftime("%j0.%y") + 'o.gz'
navfile = station + tdate.strftime("%j0.%y") + 'd.Z'
hostPath = hostPath + tdate.strftime("%Y/%j/")

ftp = FTP(server)
ftp.login()
print('FTP Login', end = '\n\n')
# print(ftp.getwelcome(), end='\n\n')

print('FTP Current Working Directory\n' + hostPath, end='\n\n')

# print('Fetching updated ephemerides')
if fetchFiles(ftp, hostPath, indir, 'igs*'):
    print('No IGS file yet')
    if fetchFiles(ftp, hostPath, indir, 'igr*'):
        print('No IGR file yet')
        if fetchFiles(ftp, hostPath, indir, 'igu*'):
            print('Not even an IGU file yet')
            print('Have a little patients!')
            
hostPath = hostPath + station
print('FTP Current Working Directory\n' + hostPath, end='\n\n')

print('FTP List')
ftp.retrlines('LIST')
print()

# print('Fetching station broadcasts')
if fetchFiles(ftp, hostPath, indir):
    print('No data files yet')

ftp.quit()


#------------------------------------------------------------------------------ 
# Decompress downloaded files
#------------------------------------------------------------------------------ 
# print('Uncompressing fetched data')
subprocess.check_output(['gzip', '-d', '-f', '-r', indir])


#------------------------------------------------------------------------------ 
# Sort downloaded files
#------------------------------------------------------------------------------ 
os.chdir(indir)
for file in os.listdir("."):
    if file.endswith(".nav"):
        navfile = file
    if file.endswith(".13o"):
        o13file = file
    if file.endswith(".sp3"):
        sp3file = file
        

#------------------------------------------------------------------------------ 
# Run RTKLIB process 
#------------------------------------------------------------------------------ 
# print('Running RTK solution')        
command1 = ([rnx2rtkp,'-k', indir + 'rtkoptions.conf','-o', outdir + namefile + '.pos', indir + obsfile, indir + navfile, indir + o13file, indir + sp3file])
command2 = ([pos2kml, outdir + namefile + '.pos'])
command3 = ([google_earth, outdir + namefile + '.kml'])


print('\nRunning ')
print(' '.join(command1))
subprocess.check_output(command1)
print('\nRunning ')
print(' '.join(command2))
subprocess.check_output(command2)
# print(' '.join(command3))
# subprocess.check_output(command3)