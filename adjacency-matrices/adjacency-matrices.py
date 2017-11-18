#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:18:20 2017

@author: Thomas Varley

This library is meant to facilitate the creation of adjacency matrices for graph analysis . 
Primarily meant to be used by neuroscientists interested in brain functional networks. 
The project is a work in progress - more functions will be added through time. 

These assume that you will always import numpy as np first. 
All other libraries are imported within the functions. 

I haven't tested these in Python 2.7 -- they may or may not work. 

"""

########################################################

import numpy as np

#Import specific .mat files output by CONN as numpy arrays.
def get_mat(path):
    import scipy.io as sio
    full_mat = sio.loadmat(path)
    return full_mat

#Takes the .mat file imported by get_mat() and extracts all the time series. 
    #Low and High are the boundries of the set of ROIs.
    #Remember when Python is inclusive and exclusive!
def mat_to_npy(full_mat, low, high):
    data = full_mat['data']
    data = data.ravel()
    data = data[low:high]
    dataset = data[0]
    for i in range(1,(high-low)):
        column = data[i]
        dataset = np.concatenate((dataset, column), axis=1)
    return dataset

#CONN outputs are concatenated across sessions: this undoes that. 
    #First and last are the first slice and last slice of the session respectively.
def seperate_conditions(dataset, first, last):
    dataset = dataset[first:last, :]
    return dataset

#Creates a standard ROI-ROI adjacency matrix. 
def create_adj_mat(dataset):
    from scipy import stats
    dataset_T = dataset.T
    adjacency = []
    length = len(dataset_T)
    for i in range(length):
        i_list = []
        for j in range(length):
            corr = stats.pearsonr(dataset_T[i], dataset_T[j])
            i_list.append(corr[0])
        adjacency.append(i_list)
    adjacency = np.array(adjacency)
    return adjacency

#Creates a sparce adjacency matrix: only significant correlations (p < alpha)
def sig_adj_mat(dataset, alpha):
    from scipy import stats
    dataset_T = dataset.T
    adjacency = []
    length = len(dataset_T)
    for i in range(length):
        i_list = []
        for j in range(length):
            corr = stats.pearsonr(dataset_T[i], dataset_T[j])
            if corr[1] < alpha:
                i_list.append(corr[0])
            else:
                i_list.append(0)
        adjacency.append(i_list)
    adjacency = np.array(adjacency)
    return adjacency

#Sliding window method of generating adjacency matrices
def sliding_adj_mat(dataset, window, TR, name):
    from scipy import stats
    k = window // TR
    m = 0
    n = 0
    while n <= len(dataset):
        n = m + k
        adjacency = []
        subset = dataset[m:n]
        subset_T = subset.T
        length = len(subset_T)
        for i in range(length):
            i_list = []
            for j in range(length):
                corr = stats.pearsonr(subset_T[i], subset_T[j])
                i_list.append(corr[0])
            adjacency.append(i_list)
        adjacency = np.array(adjacency)
        np.save(name + 'adj_mat' + str(m), adjacency)
        m += 1
        
#Sliding window w/ significance filter 
def sliding_sig_mat(dataset, alpha, window, TR, name):
    from scipy import stats 
    k = window // TR
    m = 0
    n = 0
    while n <= len(dataset):
        n = m+k
        adjacency = []
        subset = dataset[m:n]
        subset_T = subset.T
        length = len(subset_T)
        for i in range(length):
            i_list = []
            for j in range(length):
                corr = stats.pearsonr(subset_T[i], subset_T[j])
                if corr[1] < alpha:
                    i_list.append(corr[0])
                else:
                    i_list.append(0)
            adjacency.append(i_list)
        adjacency = np.array(adjacency)
        np.save(name + 'adj_mat' + str(m), adjacency)
        m += 1

#Turns all the diagonal 1s into 0s.
    #Does not output a new matrix - it modifies the input directly. 
def diagonal_zeros(dataset):
    length = len(dataset)
    for i in range(length):
        dataset[i, i] = 0
    return dataset

#Turns all entries below a given percentile (x) to 0.
def threshold(dataset, x): #x must be an integer between 0 and 100.
    from copy import copy
    t_dataset = copy(dataset)
    threshold = np.percentile(t_dataset, x)
    t_dataset[t_dataset<threshold] = 0
    return t_dataset

def binarize_mat(dataset, keep_neg):
    from copy import copy
    bin_mat = copy(dataset)
    if keep_neg == True:
        bin_mat[bin_mat > 0] = 1
        bin_mat[bin_mat < 0] = -1
        return bin_mat
    elif keep_neg == False:
        bin_mat[bin_mat > 0] = 1
        bin_mat[bin_mat < 0] = 0
    return bin_mat
    
########################################################
#Example workflow
#Returns binary adjacency matrices of only significant correlations (p<0.01), thresholded at 90%

import os

for file in os.listdir('/data/tfv21/ds133_R1.0.0/full_modafinil/roi-timeseries'):
    if file.endswith('.mat'):
        
            name = file[4:15]
        
            full_mat = get_mat(file)
        
            dataset = mat_to_npy(full_mat, 3, 135)
        
            condition000 = seperate_conditions(dataset, 0, 145)
            condition001 = seperate_conditions(dataset, 145, 291)


            condition_list = [condition000, condition001]
            str_condition_list = ['condition000', 'condition001']
            length = len(condition_list)
        
            for i in range(length):
                adj_mat = sig_adj_mat(condition_list[i], 0.01)
                adj_mat = diagonal_zeros(adj_mat)
                adj_mat = threshold(adj_mat, 90)
                adj_mat = binarize_mat(adj_mat, keep_neg = False)
                np.save(name + '_' + str_condition_list[i] + '_adj_mat', adj_mat)

#The matrices are saved as .npy files in the working directory.
#They should be ready for further analysis.