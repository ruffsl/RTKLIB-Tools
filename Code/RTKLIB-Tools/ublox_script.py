'''
Created on Jun 10, 2013

@author: whitemrj
'''
from symbol import if_stmt
import ftplib

if __name__ == '__main__':
    pass

from ftplib import FTP
import subprocess
import os, sys
import locale
from datetime import datetime
# import time

encoding = locale.getdefaultlocale()[1]
#------------------------------------------------------------------------------ 
# File Directory
#------------------------------------------------------------------------------ 
indir = '/home/ruffin/Documents/Data/in/'
outdir = '/home/ruffin/Documents/Data/out/'
server = 'ftp.ngs.noaa.gov'
hostPath = '/cors/rinex/'
station = 'paap'
rnx2rtkp = '/home/ruffin/git/rtklib/app/rnx2rtkp/gcc/rnx2rtkp'
pos2kml = '/home/ruffin/git/rtklib/app/pos2kml/gcc/pos2kml'
google_eartch = '/usr/bin/google-earth'



#------------------------------------------------------------------------------ 
# Check output directory can be dumped to
#------------------------------------------------------------------------------ 
if not outdir.endswith('/'):
    outdir += '/'
if not os.path.exists(outdir):
    os.makedirs(outdir)

#------------------------------------------------------------------------------ 
# Get log gps time from rinex file
#------------------------------------------------------------------------------ 
os.chdir(indir)
for file in os.listdir("."):
    if file.endswith(".obs"):
        obsfile = file
        namefile = os.path.splitext(obsfile)[0]
print('File name base found to be: ' + namefile, end='\n/n')

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

corfile = station + tdate.strftime("%j0.%y") + 'o.gz'
navfile = station + tdate.strftime("%j0.%y") + 'd.Z'

'''
ftp = FTP(server)
ftp.login()
print('FTP Login')
print(ftp.getwelcome(), end='\n\n')

hostPath = hostPath + tdate.strftime("%Y/%j/")
print('FTP Current Working Directory\n' + hostPath, end='\n\n')
ftp.cwd(hostPath)

try:
    list = ftp.nlst('igs*')
    for filename in list:
        fhandle = open(os.path.join(indir, filename), 'wb')
        print('Getting ' + filename)
        ftp.retrbinary('RETR ' + filename, fhandle.write)
        fhandle.close()
        igfile = filename
except ftplib.error_perm:
    print('No IGS file yet', end='\n\n')
    try:
        list = ftp.nlst('igr*')
        for filename in list:
            fhandle = open(os.path.join(indir, filename), 'wb')
            print('Getting ' + filename)
            ftp.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()
            igfile = filename
    except ftplib.error_perm:
        print('No IGR file yet', end='\n\n')
        try:
            list = ftp.nlst('igu*')
            for filename in list:
                fhandle = open(os.path.join(indir, filename), 'wb')
                print('Getting ' + filename)
                ftp.retrbinary('RETR ' + filename, fhandle.write)
                fhandle.close()
                igfile = filename
        except ftplib.error_perm:
            print('No IGU files yet')
            print('Be patient man!', end='\n\n')
            

hostPath = hostPath + station
print('FTP Current Working Directory\n' + hostPath, end='\n\n')
ftp.cwd(hostPath)
print('FTP List')
ftp.retrlines('LIST')
 
try:
    for filename in ftp.nlst():
        fhandle = open(os.path.join(indir, filename), 'wb')
        print('Getting ' + filename)
        ftp.retrbinary('RETR ' + filename, fhandle.write)
        fhandle.close()
except ftplib.error_perm:
    print('No data files yet')

ftp.quit()
'''


#------------------------------------------------------------------------------ 
# Decompress downloaded files
#------------------------------------------------------------------------------ 
subprocess.check_output(['gzip', '-d', '-r', indir])

#------------------------------------------------------------------------------ 
# Decompress downloaded files
#------------------------------------------------------------------------------ 
os.chdir(indir)
for file in os.listdir("."):
    if file.endswith(".nav"):
        navfile = file
    if file.endswith(".13o"):
        o13file = file
    if file.endswith(".sp3"):
        sp3file = file
        
command1 = ([rnx2rtkp,'-k', indir + 'rtkoptions.conf','-o', outdir + namefile + '.pos', indir + obsfile, indir + navfile, indir + o13file, indir + sp3file])
command2 = ([pos2kml, outdir + namefile + '.pos'])
command3 = ([google_eartch, outdir + namefile + '.kml'])


print('Running ')
print(' '.join(command1))
subprocess.check_output(command1)
print(' '.join(command2))
subprocess.check_output(command2)
print(' '.join(command3))
subprocess.check_output(command3)


# print('Starting ublox script\n')
# print('Checking ublox logs\n')
# print('Converting ublox logs\n')
# print('Parsing time from data\n')
# print('Fetching NOAA CORS corrections\n')
# print('Fetching station broadcasts\n')
# print('Fetching updated ephemerides\n')
# print('Uncompressing fetched data\n')
# print('Running RTK solution\n')