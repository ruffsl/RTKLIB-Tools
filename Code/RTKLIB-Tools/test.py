'''
Created on Jun 14, 2013

@author: ruffin
'''


if __name__ == '__main__':
    pass

suffix = 'wow!!!';
print(suffix)
print(suffix.endswith(suffix))

weight = float(input("How many pounds does your suitcase weigh? "))
if weight > 50:
    print("There is a $25 charge for luggage that heavy.")
print("Thank you for your business.")

# 
# num = int(ymdhms.split()[0])
# print(num)
# print(type(num))

# 
# print (tdate.strftime("%d-%b-%Y %H:%M:%S"))
# print (tnow.strftime("%d-%b-%Y %H:%M:%S"))


# lol = subprocess.Popen('ls', cwd= outdir)
# lol.wait()
# print(lol.stdout)
# subprocess.call(['ls', '-l'])
# output = subprocess.check_output('grep "TIME OF FIRST OBS" /home/ruffin/Documents/Data/in/COM10_130604_230821.obs')


# fcorfile = open(indir + corfile,'wb')  
# ftp.retrbinary('RETR ' + corfile, fcorfile.write)
# fcorfile.close()


# subprocess.check_output(['rnx2rtkp','-k', indir + 'rtkoptions.conf','-o', outdir + namefile + '.pos', indir + obsfile, indir + navfile, indir + sp3file, '-d', '-r', indir])
# subprocess.check_output(['gzip', '-d', '-r', indir])
# 
# pos2kml COM10_130604_230821.pos

 # rnx2rtkp -k rtkoptions.conf -o COM10_130604_230821.pos COM10_130604_230821.obs COM10_130604_230821.nav  paap1550.13o igr17432.sp3 
# pos2kml COM10_130604_230821.pos


# subprocess.check_output(' '.join(command1), shell=True)
# subprocess.check_output(' '.join(command2), shell=True)