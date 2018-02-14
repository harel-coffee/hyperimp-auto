#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 13:42:43 2018

@author: hildeweerts
"""

import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


def kde(df, param, bandwidth, log, intg, **kwargs):
    """ evaluate kernel denisity estimates of df[param] of a set of points
        
        Parameters
        ----------
        steps : integer, optional, default 20
    """    
    # fit kde
    if log:
        data = np.log10(df[param].as_matrix().transpose())
    else: 
        data = df[param].as_matrix().transpose()
    kde = stats.gaussian_kde(data, bw_method = bandwidth/data.std(ddof=1))
    
    # define set of points
    x_min = min(data)
    x_max = max(data)
    
    if intg:
        steps = kwargs.get('steps', int(x_max - x_min + 1))
    else:
        steps = kwargs.get('steps', 20)
    
    x = np.linspace(x_min, x_max, steps)
    
    # compute estimates
    estimates = kde.evaluate(x)
    if log:
        x = 10**x
    return x, estimates

def plot_kde(x, y, alg, param, log):
    plt.plot(x,y, '-o')
    plt.ylim(0,)
    plt.ylabel('density')
    plt.xlabel('%s__%s' % (alg, param))
    if log:
        plt.xticks(x)
        plt.xscale('log')
    plt.savefig('figures/kdes/kde__%s__%s.eps' % (alg, param),
                format = 'eps')
    plt.show()
    return
