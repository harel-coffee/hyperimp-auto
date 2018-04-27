#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 16:56:29 2018

@author: hildeweerts
"""

"""
A set of functions that can be used to evaluate the results from the importance
of tuning experiments.
"""

import scipy
import numpy as np

def tunability(x, y):
    """
    Compute the tunability of a hyperparameter.
        
        d_ij = risk_f - risk_nf
        
    where risk_f and risk_nf are the observed risk in respectively 
    fixed and non-fixed condition.
    
    Parameters
    ----------
    x : array_like
        first set of RISK observations
        
    y : array_like
        second set of RISK observations
        
    Returns
    -------
    (scores, average) : tuple with list and float
        the tunability for each of the observations as well as the average 
        tunability
    """
    x, y = map(np.asarray, (x, y))
    scores  = [a - b for a, b in zip(x, y)]
    average = np.mean(scores)
    return scores, average

def relative_tunability(x, y):
    """
    Compute the tunability of a hyperparameter.
        
        d_ij = (risk_f - risk_nf)/risk_nf
        
    where risk_f and risk_nf are the observed risk in respectively 
    fixed and non-fixed condition.
    
    Parameters
    ----------
    x : array_like
        first set of RISK observations
        
    y : array_like
        second set of RISK observations
        
    Returns
    -------
    (scores, average) : tuple with list and float
        the relative tunability for each of the observations as well as the 
        average relative tunability
    """
    x, y = map(np.asarray, (x, y))
    scores  = [(a - b)/b for a, b in zip(x, y)]
    average = np.mean(scores)
    return scores, average

def noninferior(x, y, delta, alpha):
    """
    Perform a one sided non-inferiority test for relative risk.
    
        H0: (Median_x - Median_y)/(Median_y) >= delta
        H1: (Median_x - Median_y)/(Median_y) < delta
    
    Part of this code is adapted from scipy's scipy.stats.wilcoxon.
    
    Parameters
    ----------
    x : array_like
        first set of RISK observations (not performance!)
        
    y : array_like
        second set of RISK observations (not performance!)
    
    delta : float
        non-inferiority margin
        
    alpha : float
        type 1 error rate
    """
    
    x, y = map(np.asarray, (x, y))
    if len(x) != len(y):
        raise ValueError('Unequal N in non-inferiority test. Aborting.')
    d = [(a - b)/b - delta for a, b in zip(x, y)]
    
    r = scipy.stats.rankdata(abs(d)) # ranks
    sr = np.sum((d < 0) * r, axis=0) # sum of negative ranks
    N = len(d)
    z = (sr - (N*(N+1))/4)/np.sqrt((N*(N+1)*(2*N+1))/24)
    p = distributions.norm.sf(abs(z))
    return z, p