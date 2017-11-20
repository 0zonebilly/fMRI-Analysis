# fMRI-Analysis
These are projects from my work at the University of Cambridge, in the Cognition and Consciousness Group.

All of these projects should be considered free and open-source, unless otherwise explicitly mentioned. Authorship is denoted within each file itself. While files are free to be downloaded, modified, or used, please maintain the credits and the original date of creation in all subsequent instances. 

TO DO: Poincare/return maps.

## Projects

__Lempel-Ziv Compressability & Perturbational Complexity Index__

Based on work by Casali et al., this algorithm uses the classic Lempel-Ziv compressability measure as a proxiy for the algorithmic information content of a system. The raw Lempel-Ziv compressability score can be normalized by the Shannon entropy of the source tensor to give a variation on the Perturbational Complexity Index (PCI). 

__Nodal Entropy__

Based on work by Ioannis Pappas in my lab at Cambridge and independently dervied by Viol et al., this gives a measure of the structural entropy of a brain functional connectivity network. A distribution of the degrees of every node in a graph is used to calculate a measure of entropy for the network. Used as a proxy measure for complexity. 

__Point Process Analysis__
Described by Tagliazucci et al., this system binarizes a neural timeseries, extracting only those events which surpass a given threashold (in this case, 1 standard deviation). This very efficiently compresses a network. The library also has functions for returning the rate of events, as well as the average interval between events. 

### Pipeline Code

__Adjacency Matrices__

This is a library for researchers who want to quickly and efficiently make adjacency matrices from fMRI timeseries data, such as what is returned by CONN. The library is highly modular, allowing for customizable pipelines incorporating different temporal resolutions, thresholding and binarization parameters. 

Questions can be addressed to:
tfv21@cam.ac.uk
