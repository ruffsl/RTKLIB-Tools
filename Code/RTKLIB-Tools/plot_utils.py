'''
Created on Jul 11, 2013

@author: ruffin
'''


from matplotlib import pyplot, mpl
import numpy as np
from geopy import point, distance

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if mpl.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'
