# -*- coding: utf-8 -*-
"""
Author: Thomas Varley

This implements point process analysis on a neural timeseries.

Described by Tagliazucci et al.

Tagliazucchi et al., “Enhanced Repertoire of Brain Dynamical States during the Psychedelic Experience.” Human Brain Mapping (November 1, 2014)

"""

import numpy as np

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
            
            
    
    
    