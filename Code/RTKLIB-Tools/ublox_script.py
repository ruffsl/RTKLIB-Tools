'''
Created on Jun 10, 2013

@author: whitemrj
'''
from symbol import if_stmt

if __name__ == '__main__':
    pass

from ftplib import FTP
import subprocess
import os, sys
import sh
#------------------------------------------------------------------------------ 
# File Directory
#------------------------------------------------------------------------------ 
indir = "/home/ruffin/Documents/Data/in/"
outdir = "/home/ruffin/Documents/Data/out/"
obsFile = '/home/ruffin/Documents/Data/in/COM10_130604_230821.obs'

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
lol = subprocess.Popen('./ls', cwd='/bin')
lol.wait()
print(lol.stdout)


# print(subprocess.check_output(['grep', '"TIME OF FIRST OBS"', obsFile])




# ftp = FTP('ftp.ngs.noaa.gov')
# ftp.login()
# ftp.getwelcome()
# ftp.retrlines('LIST')
# 
# file = 'paap1580.13S'
# hostPath = '/cors/rinex/2013/158/paap'
# clientPath = '/home/ruffin/Documents/Data/'
# 
# f = open(clientPath + file,'wb')  
# 
# ftp.cwd(hostPath)
# 
# ftp.retrbinary('RETR ' + file, f.write)
# f.close()
# ftp.quit()
# 
# 
# 
# print('Starting ublox script\n')
# print('Checking ublox logs\n')
# print('Converting ublox logs\n')
# print('Parsing time from data\n')
# print('Fetching NOAA CORS corrections\n')
# print('Fetching station broadcasts\n')
# print('Fetching updated ephemerides\n')
# print('Uncompressing fetched data\n')
# print('Running RTK solution\n')