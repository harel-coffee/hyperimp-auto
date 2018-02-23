#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:10:24 2018

@author: hildeweerts
"""

"""
Set of classes and functions that can be used to find the 'best' parameter settings.
"""

import pandas as pd
import numpy as np

class Alg:
    """
    An Alg object represents a classifier.
    
    Attributes
    ----------
        name : string
            name of the algorithm
        params : list of Param objects
            all hyperparameters that are associated with Alg
        perf : dataframe
            performance data of the algorithm in the following format:
            - 'task_id' : column with OpenML task id's
            - several columns with hyperparameter settings
            - 'y' : column with performance measure
            
    Methods
    -------
        add_param : add a parameter to 'params'
    """
    
    # initialize algorithm
    def __init__(self, name, params, perf):
        self.name = name
        self.params = params
        self.perf = perf
    # add a Param object to the list of parameters
    def add_param(self, param):
        self.params.append(param)
    
class Param:
    """
    A Param object represents a hyperparameter.
    
    Attributes
    ----------
        name : string
            name of the parameter
        log : boolean
            parameter on a log scale (True) or not (False)
        intg : boolean 
            parameter uses integer scale (True) or not (False)
    """
    def __init__(self, name, log, intg):
        self.name = name
        self.log = log
        self.intg = intg
        

def init_algs(fname, dfs):
    """
    Return a list of algs objects. 
    
    Parameters
    ----------
    filename : string
        directory + name of the file where parameter attributes are saved
    dfs : dictionary of dataframes
        keys : alg_name (str)
        values : performance data (pandas DataFrame)
    """
    
    # read parameters
    parameters = pd.read_csv(fname)
    alg_params = {}
    for alg_name, group in parameters.groupby('alg'):
        params = []
        for index, data in group.iterrows():
            param_name = data['param_name']
            log = data['log']
            intg = data['intg']
            params.append(Param(param_name, log, intg))
        alg_params[alg_name] = params
    
    # create Alg objects
    algs = []
    for key in alg_params.keys():
        algs.append(Alg(key, alg_params[key], dfs[key]))

    return algs
    
def find_settings(alg, n, m):
    """ 
    Estimates the 'best' hyperparameter settings of an algorithm based on 
    performance data of 100 OpenML data sets.
    
    The estimate is the largest bin of a histogram. In case of multiple 
    occurrences of the largest bin, the parameters corresponding to the first 
    occurrence are returned.
        
    Parameters
    ----------
    alg : Alg
        object of Alg class
    n : integer
        top n rows of each dataset will be used to estimate best settings
    m : integer
        minimum number of observations per dataset
        
    Returns
    -------
    settings : dictionary
        dictionary with best parameter setting for an algorithm
            key : parameter name
            value : (lower, upper, average)
                lower, upper, and average of 'best' hyperparameter setting
    """
    # get top n performance data
    groups = []
    for g in alg.perf.groupby(['task_id']):
        group = pd.DataFrame(g[1])
        group['task_id'] = g[0]
        if (len(group) > m) :
            groups.append(group.sort_values(by = 'y', ascending  = False)[0:n])
        else:
            None
            #print('Dataset %s not included because no. obervations is %s.' %(int(g[0]), int(len(group))))
    topn = pd.concat(groups)
    
    # get best setting from top n performance data for each parameter of alg
    settings = {}
    for param in alg.params:
        x = topn[param.name]
        bins = 'auto'
        rnge = None
        if param.intg:
            bins = int(max(x) - min(x) + 1)
            rnge = (int(min(x)), int(max(x) + 1))
        if param.log:
            x = np.log10(x)
        hist, bin_edges = np.histogram(x, bins = bins, range = rnge)
        index = np.argmax(hist)
        setting_lower = bin_edges[index]
        setting_upper = bin_edges[index + 1]
        setting_average = (bin_edges[index] + bin_edges[index + 1])/2
        if param.intg:
            setting_upper = bin_edges[index]
            setting_average = bin_edges[index]
        if param.log:
            setting_lower = 10**setting_lower
            setting_upper = 10**setting_upper
            setting_average = 10**setting_average
        settings[param.name] = (setting_lower, setting_upper, setting_average)
    return settings


