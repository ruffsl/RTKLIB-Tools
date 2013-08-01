'''
Created on Jul 11, 2013

@author: ruffin
'''

from matplotlib import pyplot, mpl
import pandas as pd
import scipy as sp
import numpy as np
import pylab as pl
from file_utils import *



def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if mpl.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

def neuTFPNplot(dff_test, y_, fig, tittle = 'Labeled Solutions', radius = 0.3 , aspect='equal'):
    dff_test['y_'] = y_
    
    dff_test['TFPN'] = ''
    for i in dff_test.index:
        yp = dff_test['y'][i]
        y_ = dff_test['y_'][i]
        s = ''
        if ~ (yp ^ y_):
            s += 'T'
            if y_:
                s += 'P'
            else:
                s += 'N'
        else:
            s += 'F'
            if y_:
                s += 'P'
            else:
                s += 'N'
        
        dff_test['TFPN'][i] = s
        
    dff_test_TP = dff_test[dff_test['TFPN'].str.contains("TP")]
    dff_test_TN = dff_test[dff_test['TFPN'].str.contains("TN")]
    dff_test_FP = dff_test[dff_test['TFPN'].str.contains("FP")]
    dff_test_FN = dff_test[dff_test['TFPN'].str.contains("FN")]
        
    print('Generating Fig')
    #fig = pyplot.figure(figsize=(20,18), dpi=200)
    fig.suptitle(tittle, fontsize=14, fontweight='bold')
    #ax = fig.add_subplot(111)
    ax = fig.add_subplot(1,3,1,aspect=aspect)
    p = ax.scatter(dff_test_TP['diste(m)'],dff_test_TP['distn(m)'], label= 'TP (Green) ', alpha=.1, c='green')
    p = ax.scatter(dff_test_TN['diste(m)'],dff_test_TN['distn(m)'], label= 'TN (Blue)  ', alpha=.1, c='blue')
    p = ax.scatter(dff_test_FP['diste(m)'],dff_test_FP['distn(m)'], label= 'FP (Red)   ', alpha=.1, c='red')
    p = ax.scatter(dff_test_FN['diste(m)'],dff_test_FN['distn(m)'], label= 'FN (Orange)', alpha=.1, c='orange')
    circle = Circle((0,0), radius=0.3, color='gray', fill=False)
    fig.gca().add_artist(circle)
    pl.legend(loc="lower right")
    #xlim(distnminlim, distnmaxlim)
    #ylim(disteminlim, distemaxlim)
    ax.set_xlabel('East (meters)')
    ax.set_ylabel('North (meters)')
    ax.grid(True)
 
    ax = fig.add_subplot(1,3,3,aspect=aspect)
    p = ax.scatter(dff_test_TP['distn(m)'],dff_test_TP['distu(m)'], label= 'TP (Green) ', alpha=.1, c='green')
    p = ax.scatter(dff_test_TN['distn(m)'],dff_test_TN['distu(m)'], label= 'TN (Blue)  ', alpha=.1, c='blue')
    p = ax.scatter(dff_test_FP['distn(m)'],dff_test_FP['distu(m)'], label= 'FP (Red)   ', alpha=.1, c='red')
    p = ax.scatter(dff_test_FN['distn(m)'],dff_test_FN['distu(m)'], label= 'FN (Orange)', alpha=.1, c='orange')
    circle = Circle((0,0), radius=radius, color='gray', fill=False)
    fig.gca().add_artist(circle)
    pl.legend(loc="lower right")
    #xlim(distnminlim, distnmaxlim)
    #ylim(disteminlim, distemaxlim)
    ax.set_xlabel('North (meters)')
    ax.set_ylabel('Up (meters)')
    ax.grid(True)
    
    ax = fig.add_subplot(1,3,2,aspect=aspect)
    p = ax.scatter(dff_test_TP['diste(m)'],dff_test_TP['distu(m)'], label= 'TP (Green) ', alpha=.1, c='green')
    p = ax.scatter(dff_test_TN['diste(m)'],dff_test_TN['distu(m)'], label= 'TN (Blue)  ', alpha=.1, c='blue')
    p = ax.scatter(dff_test_FP['diste(m)'],dff_test_FP['distu(m)'], label= 'FP (Red)   ', alpha=.1, c='red')
    p = ax.scatter(dff_test_FN['diste(m)'],dff_test_FN['distu(m)'], label= 'FN (Orange)', alpha=.1, c='orange')
    circle = Circle((0,0), radius=radius, color='gray', fill=False)
    fig.gca().add_artist(circle)
    pl.legend(loc="lower right")
    #xlim(distnminlim, distnmaxlim)
    #ylim(disteminlim, distemaxlim)
    ax.set_xlabel('East (meters)')
    ax.set_ylabel('Up (meters)')
    ax.grid(True)
    
def neTFPNplot(dff_test, y_, fig, tittle = 'Labeled Solutions', radius = 0.3, aspect='equal'):
    dff_test['y_'] = y_
    
    dff_test['TFPN'] = ''
    for i in dff_test.index:
        yp = dff_test['y'][i]
        y_ = dff_test['y_'][i]
        s = ''
        if ~ (yp ^ y_):
            s += 'T'
            if y_:
                s += 'P'
            else:
                s += 'N'
        else:
            s += 'F'
            if y_:
                s += 'P'
            else:
                s += 'N'
        
        dff_test['TFPN'][i] = s
        
    dff_test_TP = dff_test[dff_test['TFPN'].str.contains("TP")]
    dff_test_TN = dff_test[dff_test['TFPN'].str.contains("TN")]
    dff_test_FP = dff_test[dff_test['TFPN'].str.contains("FP")]
    dff_test_FN = dff_test[dff_test['TFPN'].str.contains("FN")]
        
    print('Generating Fig')
    #fig = pyplot.figure(figsize=(20,18), dpi=200)
    fig.suptitle(tittle, fontsize=14, fontweight='bold')
    #ax = fig.add_subplot(111)
    ax = fig.add_subplot(1,1,1,aspect=aspect)
    p = ax.scatter(dff_test_TP['diste(m)'],dff_test_TP['distn(m)'], label= 'TP (Green) ', alpha=.1, c='green')
    p = ax.scatter(dff_test_TN['diste(m)'],dff_test_TN['distn(m)'], label= 'TN (Blue)  ', alpha=.1, c='blue')
    p = ax.scatter(dff_test_FP['diste(m)'],dff_test_FP['distn(m)'], label= 'FP (Red)   ', alpha=.1, c='red')
    p = ax.scatter(dff_test_FN['diste(m)'],dff_test_FN['distn(m)'], label= 'FN (Orange)', alpha=.1, c='orange')
    circle = Circle((0,0), radius=0.3, color='gray', fill=False)
    fig.gca().add_artist(circle)
    pl.legend(loc="lower right")
    #xlim(distnminlim, distnmaxlim)
    #ylim(disteminlim, distemaxlim)
    ax.set_xlabel('East (meters)')
    ax.set_ylabel('North (meters)')
    ax.grid(True)