#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 13:07:23 2017

@author: Thomas Varley 

Calculates the nodal entropy of a full correlation matrix.
Inspired by:
Ioannis Pappas @ Dept. of Clinical Neurosciences, Cambridge University 
Viol et .al, @ Universidade Federal do Rio Grande do Norte

Viol et al., “Shannon Entropy of Brain Functional Complex Networks under the Influence of the Psychedelic Ayahuasca.” Scientific Reports, (August 7, 2017).

All matrices must be in .npy format 
The entropy is calculated using the natural log rather than log base 2.
This only works in Python 3+

"""

import numpy as np
import networkx as nx
import os
import math
from scipy import stats

###################################################################

#Creates the nodal degree list
def degree_list(graph):
    degree_list = []
    degree_dic = graph.degree()
    for degree in degree_dic:
        degree_list.append(degree[1])
    return degree_list

#Creates the histogram of nodal degrees
def hist(source):
    histogram = {}; length = 0;
    for entry in source:
        length += 1
        if entry not in histogram:
            histogram[entry] = 0
        histogram[entry] += 1
    return(length, histogram)
    
#Calculates entropy of the nodal degrees
def entropy(source):
    length, histogram = hist(source)
    e_list = []
    for value in histogram.values():
        p = value / length
        e_list.append(-p * math.log(p))
    return sum(e_list)

#Returns the nodal entropy from a raw adjacency matrix
def matrix_nodal_entropy(dataset):
    graph = nx.from_numpy_matrix(dataset)    
    deg_list = degree_list(graph)    
    ent = entropy(deg_list)
    return ent

#Returns the nodal entropy from a networkx graph
def nodal_entropy(graph):
    deg_list = degree_list(graph)
    ent = entropy(deg_list)
    return ent
    
    
###################################################################

#Create the vector of entropies for all Condition Networks

#Importing the file and processing the adjacency matrix

entropies = []

for file in os.listdir("path/to/directory/"):
    if file.endswith("*.npy"):
        dataset = np.load(file)
        ent = matrix_nodal_entropy(dataset, int)
        entropies.append(ent)
