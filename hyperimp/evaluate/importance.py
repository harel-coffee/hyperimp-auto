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
from scipy.stats import rankdata, distributions

def get_val_scores(trace):
    """
    For each iteration of a run, compute the maximum validation score up until 
    that iteration.
    
    Parameters
    ----------
    trace : OpenMLTrace object
        trace object that can be retrieved using openml.runs.get_run_trace(run_id)
        
    Returns
    -------
    val_scores : list
        a list of maximum validation scores for each iteration from 0 up until 99
    """
    val_scores = []
    val_max = 0
    for iteration in range(0,100):
        # compute average validation score for this iteration
        val_sum = 0
        for fold in range(0,10):
            val_sum += trace.trace_iterations[(0, fold, iteration)].evaluation
        val_avg = val_sum/10
        # check if new validation average is larger than the current maximum
        if val_avg > val_max:
            val_max = val_avg
        # store current maximum for iteration
        val_scores.append(val_max)
    return val_scores


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
    return scores

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
    scores = []
    scores = [(a-b)/b for a, b in zip(x,y)]
    return scores

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
    if len(x) != len(y):
        raise ValueError('Unequal N in non-inferiority test. Aborting.')
    d = [(a - b)/b - delta for a, b in zip(x, y)]
    r = rankdata(np.abs(d)) # ranks
    sr = np.sum([x < 0 for x in d] * r) # sum of negative ranks
    N = len(d)
    z = (sr - (N*(N+1))/4)/np.sqrt((N*(N+1)*(2*N+1))/24)
    p = distributions.norm.sf(np.abs(z))
    return z, p

def equivalence(x, y, delta, alpha):
    """
    Perform two one sided non-inferiority tests for relative risk.
    
    hypothesis 1:
        H0: (Median_x - Median_y)/(Median_y) >= delta
        H1: (Median_x - Median_y)/(Median_y) < delta
    
    hypothesis 2:
        H0: (Median_x - Median_y)/(Median_y) >= - delta
        H1: (Median_x - Median_y)/(Median_y) < -delta

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
    if len(x) != len(y):
        raise ValueError('Unequal N in equivalence test. Aborting.')
    N = len(x)
    
    # test 1
    d1 = [(a - b)/b - delta for a, b in zip(x, y)]
    r1 = rankdata(np.abs(d1)) # compute signed ranks
    sr1 = np.sum([x < 0 for x in d1] * r1) # absolute sum of negative ranks
    z1 = (sr1 - (N*(N+1))/4)/np.sqrt((N*(N+1)*(2*N+1))/24)
    p1 = distributions.norm.sf(np.abs(z1))
    
    # test 2
    d2 = [(a - b)/b - (-delta) for a, b in zip(x, y)]
    r2 = rankdata(np.abs(d2)) # compute signed ranks
    sr2 = np.sum([x > 0 for x in d2] * r2) # sum of positive ranks
    z2 = (sr2 - (N*(N+1))/4)/np.sqrt((N*(N+1)*(2*N+1))/24)
    p2 = distributions.norm.sf(np.abs(z2))
    return z1, p1, z2, p2

def equivalence_nonrel(x, y, delta, alpha):
    """
    Perform two one sided non-inferiority tests for relative risk.
    
    hypothesis 1:
        H0: (Median_x - Median_y)/(Median_y) >= delta
        H1: (Median_x - Median_y)/(Median_y) < delta
    
    hypothesis 2:
        H0: (Median_x - Median_y)/(Median_y) >= - delta
        H1: (Median_x - Median_y)/(Median_y) < -delta

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
    if len(x) != len(y):
        raise ValueError('Unequal N in equivalence test. Aborting.')
    N = len(x)
    
    # test 1
    d1 = [(a - b) - delta for a, b in zip(x, y)]
    r1 = rankdata(np.abs(d1)) # compute signed ranks
    sr1 = np.sum([x < 0 for x in d1] * r1) # absolute sum of negative ranks
    z1 = (sr1 - (N*(N+1))/4)/np.sqrt((N*(N+1)*(2*N+1))/24)
    p1 = distributions.norm.sf(np.abs(z1))
    
    # test 2
    d2 = [(a - b) - (-delta) for a, b in zip(x, y)]
    r2 = rankdata(np.abs(d2)) # compute signed ranks
    sr2 = np.sum([x > 0 for x in d2] * r2) # sum of positive ranks
    z2 = (sr2 - (N*(N+1))/4)/np.sqrt((N*(N+1)*(2*N+1))/24)
    p2 = distributions.norm.sf(np.abs(z2))
    return z1, p1, z2, p2

