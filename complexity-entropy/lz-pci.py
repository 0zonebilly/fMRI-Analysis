reated on Fri Nov 17 21:08:08 2017

@author: Thomas Varley

LZ Complexity code based on work by Lilian Besson.
PCI normalization factor based on work by Leonardo Barbarosa

Python implementation of the Perturbational Complexity Index
Casali et al., "A Theoretically Based Index of Consciousness Independent of Sensory Processing and Behavior" Science Translational Medicine (August 14th, 2013)

This will only work in Python 3+
"""

import numpy as np

#Returns the Lempel-Ziv complexity of a binary string. 
def lz_string(binary_string):
    u = 0
    v = 1
    w = 1
    v_max = 1
    length = len(binary_string)
    complexity = 1
    while True:
        if binary_string[u + v - 1] == binary_string[w + v - 1]:
            v += 1
            if w + v >= length:
                complexity += 1
                break
        else:
            if v > v_max:
                v_max = v
            u += 1
            if u == w:
                complexity += 1
                w += v_max
                if w > length:
                    break
                else:
                    u = 0
                    v = 1
                    v_max = 1
            else:
                v = 1
    return complexity

#Takes a binary tensor and flattens it, passing the string to lz_string()
def lz_complexity(dataset):
    string = ''
    vector = dataset.flatten()
    length = len(vector)
    vector = vector.astype(dtype = np.int64)
    for i in range(length):
        string += str(vector[i])
    complexity = lz_string(string)
    return complexity

#Calculates the Shannon entropy of a binary tensor
def source_entropy(dataset):
    import math
    vector = dataset.flatten()
    length = len(vector)
    p_1 = sum(vector)/length 
    p_0 = 1 - p_1
    ent = -p_1 * math.log(p_1, 2) -p_0 * math.log(p_0, 2)
    norm_factor = (length * ent) / math.log(length, 2)
    return norm_factor

#Normalizes the Lempel-Ziv complexity by dividing it by the Shannon entropy of the original tensor. 
def PCI(dataset):
    return lz_complexity(dataset) / source_entropy(dataset)
    
