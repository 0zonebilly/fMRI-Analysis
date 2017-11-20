# -*- coding: utf-8 -*-
"""
Author: Thomas Varley

This implements point process analysis on a neural timeseries.
2D and 3D implementations of a Poincare return map are included, for use on the processed timeseries. 

Described by Tagliazucci et al.

Tagliazucchi et al., “Enhanced Repertoire of Brain Dynamical States during the Psychedelic Experience.” Human Brain Mapping (November 1, 2014)

"""

import numpy as np

####################################################
#Point Process Analysis
####################################################


def point_process(timeseries):
    from copy import copy
    series = copy(timeseries)
    mean = np.mean(timeseries)
    std = np.std(timeseries)
    threshold = std + mean
    series[series < threshold] = 0
    series[series >= threshold] = 1
    return series

def ppa_rate(timeseries):
    from copy import copy
    series = copy(timeseries)
    mean = np.mean(timeseries)
    std = np.std(timeseries)
    threshold = std + mean
    
    series[series < threshold] = 0
    series[series >= threshold] = 1
    
    length = len(series)
    rate = sum(series) / length 
    return rate 

def ppa_interval(timeseries):
    from copy import copy
    series = copy(timeseries)
    mean = np.mean(timeseries)
    std = np.std(timeseries)
    threshold = std + mean
    
    series[series < threshold] = 0
    series[series >= threshold] = 1
    
    length = len(series)
    intervals = []
    
    i = 0
    counter = 0
    
    while i < length:
        if series[i] == 1:
            intervals.append(counter)
            counter = 0
            i += 1
        elif series[i] == 0:
            counter += 1
            i += 1
    return np.mean(intervals)

####################################################
#Poincare Return Maps
####################################################

#Returns the interval, in seconds, between one event and the next
def interval(timeseries, TR):
    length = len(timeseries)
    intervals = []
    i = 0
    counter = 0
    
    while i < length:
        if timeseries[i] == 1:
            intervals.append(counter)
            counter = 0
            i += 1
        elif timeseries[i] == 0:
            counter += 1
            i += 1
    intervals = [TR*x for x in intervals]
    return intervals

#Creates a 2D Poincare return map of the binary timeseries
def poincare_return_2D(timeseries, TR):
    import matplotlib as plt
    length = len(timeseries)
    intervals = []
    i = 0
    counter = 0
    
    while i < length:
        if timeseries[i] == 1:
            intervals.append(counter)
            counter = 0
            i += 1
        elif timeseries[i] == 0:
            counter += 1
            i += 1
    x_axis = [TR*x for x in intervals]
    y_axis = x_axis[1:]
    x_axis = x_axis[:-1]
    
    plt.pyplot.scatter(x_axis, y_axis)

#Creates a 3D Poincare return map of the binary timeseries
def poincare_return_3D(timeseries, TR):
    from matplotlib import pyplot
    from mpl_toolkits.mplot3d import Axes3D
    
    length = len(timeseries)
    intervals = []
    i = 0
    counter = 0
    
    while i < length:
        if timeseries[i] == 1:
            intervals.append(counter)
            counter = 0
            i += 1
        elif timeseries[i] == 0:
            counter += 1
            i += 1
    x_axis = [TR*x for x in intervals]
    y_axis = x_axis[1:-1]
    z_axis = x_axis[2:]
    x_axis = x_axis[:-2]
    
    fig = pyplot.figure()
    ax = Axes3D(fig)
    
    ax.scatter(x_axis, y_axis, z_axis)
    pyplot.show()
