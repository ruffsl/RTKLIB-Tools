'''
Created on Jun 14, 2013

@author: ruffin
'''


if __name__ == '__main__':
    pass

import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as spatial

def fmt(x, y):
    return 'x: {x:0.2f}\ny: {y:0.2f}'.format(x=x, y=y)

class FollowDotCursor(object):
    """Display the x,y location of the nearest data point.
    """
    def __init__(self, ax, x, y, tolerance=5, formatter=fmt, offsets=(-20, 20)):
        try:
            x = np.asarray(x, dtype='float')
        except (TypeError, ValueError):
            x = np.asarray(mdates.date2num(x), dtype='float')
        y = np.asarray(y, dtype='float')
        self._points = np.column_stack((x, y))
        self.offsets = offsets
        self.scale = x.ptp()
        self.scale = y.ptp() / self.scale if self.scale else 1
        self.tree = spatial.cKDTree(self.scaled(self._points))
        self.formatter = formatter
        self.tolerance = tolerance
        self.ax = ax
        self.fig = ax.figure
        self.ax.xaxis.set_label_position('top')
        self.dot = ax.scatter(
            [x.min()], [y.min()], s=130, color='green', alpha=0.7)
        self.annotation = self.setup_annotation()
        plt.connect('motion_notify_event', self)

    def scaled(self, points):
        points = np.asarray(points)
        return points * (self.scale, 1)

    def __call__(self, event):
        ax = self.ax
        # event.inaxes is always the current axis. If you use twinx, ax could be
        # a different axis.
        if event.inaxes == ax:
            x, y = event.xdata, event.ydata
        elif event.inaxes is None:
            return
        else:
            inv = ax.transData.inverted()
            x, y = inv.transform([(event.x, event.y)]).ravel()
        annotation = self.annotation
        x, y = self.snap(x, y)
        annotation.xy = x, y
        annotation.set_text(self.formatter(x, y))
        self.dot.set_offsets((x, y))
        bbox = ax.viewLim
        event.canvas.draw()

    def setup_annotation(self):
        """Draw and hide the annotation box."""
        annotation = self.ax.annotate(
            '', xy=(0, 0), ha = 'right',
            xytext = self.offsets, textcoords = 'offset points', va = 'bottom',
            bbox = dict(
                boxstyle='round,pad=0.5', fc='yellow', alpha=0.75),
            arrowprops = dict(
                arrowstyle='->', connectionstyle='arc3,rad=0'))
        return annotation

    def snap(self, x, y):
        """Return the value in self.tree closest to x, y."""
        dist, idx = self.tree.query(self.scaled((x, y)), k=1, p=1)
        try:
            return self._points[idx]
        except IndexError:
            # IndexError: index out of bounds
            return self._points[0]

x = np.random.normal(0,1.0,100)
y = np.random.normal(0,1.0,100)
fig, ax = plt.subplots()

cursor = FollowDotCursor(ax, x, y, formatter=fmt, tolerance=20)
scatter_plot = plt.scatter(x, y, facecolor="b", marker="o")

#update the colour 
new_facecolors = ["r","g"]*50
scatter_plot.set_facecolors(new_facecolors)    

plt.show()

# suffix = 'wow!!!';
# print(suffix)
# print(suffix.endswith(suffix))
# 
# weight = float(input("How many pounds does your suitcase weigh? "))
# if weight > 50:
#     print("There is a $25 charge for luggage that heavy.")
# print("Thank you for your business.")

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