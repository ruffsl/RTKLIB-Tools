'''
Created on Jun 10, 2013

@author: whitemrj
'''

if __name__ == '__main__':
    pass

from ftplib import FTP
ftp = FTP('ftp.ngs.noaa.gov')
ftp.login()
ftp.getwelcome()
ftp.retrlines('LIST')

file = 'paap1580.13S'
hostPath = '/cors/rinex/2013/158/paap'
clientPath = '/home/ruffin/Documents/Data/'

f = open(clientPath + file,'wb')  

ftp.cwd(hostPath)

ftp.retrbinary('RETR ' + file, f.write)



# ftp.retrbinary("RETR paap1580.13S", open('paap1580.13S', 'wb').write)

f.close()
ftp.quit()

# ftp://www.ngs.noaa.gov/cors/rinex/2013/158/paap/paap1580.13S

print('Starting ublox script\n')
print('Checking ublox logs\n')
print('Converting ublox logs\n')
print('Parsing time from data\n')
print('Fetching NOAA CORS corrections\n')
print('Fetching station broadcasts\n')
print('Fetching updated ephemerides\n')
print('Uncompressing fetched data\n')
print('Running RTK solution\n')