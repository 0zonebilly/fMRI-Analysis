#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:08:08 2017

@author: Thomas Varley

LZ Complexity code based on work by Lilian Besson @ CentraleSupélec, Rennes, France
PCI normalization factor based on work by Leonardo Barbarosa @ University of Wisconsin-Madison

Python implementation of the Perturbational Complexity Index
Casali et al., "A Theoretically Based Index of Consciousness Independent of Sensory Processing and Behavior" Science Translational Medicine (August 14th, 2013)

This will only work in Python 3+
"""

import numpy as np

#Returns the Lempel-Ziv complexity of a binary string. 
def lz_string(string):

 d={} 
 w = ''
 i=1
 for c in string: 
  wc = w + c
  if wc in d:
   w = wc
  else:
   d[wc]=wc
   w = c
  i+=1
 return len(d)

#Takes a binary tensor and flattens it, passing the string to lz_string()
def lz_complexity(dataset):
    string = ''
    vector = dataset.ravel()
    length = len(vector)
    vector = vector.astype(dtype = np.int64)
    for i in range(length):
        string += str(vector[i])
    complexity = lz_string(string)
    return complexity

#Calculates the Shannon entropy of a binary tensor
def source_entropy(dataset):
    import math
    vector = dataset.ravel()
    length = len(vector)
    p_1 = sum(vector)/length 
    p_0 = 1 - p_1
    ent = -p_1 * math.log(p_1, 2) -p_0 * math.log(p_0, 2)
    norm_factor = (length * ent) / math.log(length, 2)
    return norm_factor

#Normalizes the Lempel-Ziv complexity by dividing it by the Shannon entropy of the original tensor. 
def PCI(dataset):
    return lz_complexity(dataset) / source_entropy(dataset)
    
