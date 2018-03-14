#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:31:15 2018

@author: hildeweerts
"""

"""
Generate dictionary with parameter ranges for random search that can be used
for RandomSearchCV() in ScikitLearn.
"""

import numpy as np
import pickle
from hyperimp.utils.distributions import loguniform_gen, loguniform_int_gen
from scipy.stats import uniform, randint

def init_search_space():
    """ 
    Returns
    -------
    Dictionary with for each alg and parameter a random variable object (continuous 
    parameters) or a list of values (nominal parameters).
    
    {alg1 : {param1 : XXX,
             param2 : XXX},
     alg2 : ...}
    """
    search_space = {
        # Parameters where just one fixed value is considered
        ('svm', 'kernel') : {
                'type' : 'fix',
                'domain' : ['rbf']},
                
        ('random_forest', 'n_features') : {
                'type' : 'fix',
                'domain' : [500]},
        
        # Parameters where a range of parameter settings is considered
        ('svm', 'gamma') : {
                'type' : 'log2',
                'min' : 2**-15,
                'max' : 2**3},
                
        ('svm', 'C') : {
                'type' : 'log2',
                'min' : 2**-5,
                'max' : 2**15},
                
        ('svm', 'tol') : {
                'type' : 'log10',
                'min' : 10**-5,
                'max' : 10**-1},
                
        ('svm', 'coef0') : {
                'type' : 'lin',
                'min' : 0,
                'max' : 1},
        
        ('svm', 'shrinking') : {
                'type' : 'nom',
                'domain' : [True, False]},

        ('random_forest', 'bootstrap') : {
                'type' : 'nom',
                'domain' : [True, False]},
        
        ('random_forest', 'criterion') : {
                'type' : 'nom',
                'domain' : ['gini', 'entropy']},
        
        ('random_forest', 'max_features') : {
                'type' : 'lin',
                'min' : 0, # n ** 0
                'max' : 1}, # n ** 1
                
        ('random_forest', 'min_samples_leaf') : {
                'type' : 'int',
                'min' : 1,
                'max' : 20},
                
        ('random_forest', 'min_samples_split') : {
                'type' : 'int',
                'min' : 2,
                'max' : 20}
        }
    
    # Initialize loguniform objects
    loguniform = loguniform_gen(name='loguniform')
    loguniform_int = loguniform_int_gen(name = 'loguniform_int')
    
    search_space_rv = {}
    for (alg, param_name), param in search_space.items():
        if param['type'] == 'int':
            rv = randint(low = param['min'], high = param['max'] + 1)
        elif param['type'] == 'log2': 
            rv = loguniform(base = 2, low = param['min'], high = param['max'])
        elif param['type'] == 'log10':
            rv = loguniform(base = 10, low = param['min'], high = param['max'])
        elif param['type'] == 'lin':
            rv = uniform(loc = param['min'], scale = param['max'] - param['min'])
        elif param['type'] == 'nom' or param['type'] == 'fix':
            rv = param['domain']
        elif param['type'] == 'exp':
            rv = None
            print("Warning: could not add '%s' because type 'exp' is not implemented." % param_name)
            #raise NotImplementedError()
        else:
            raise ValueError()
            
        if alg in search_space_rv:
            search_space_rv[alg][param_name] = rv
        else:
            search_space_rv[alg] = {param_name : rv}
    return search_space_rv

if __name__ == '__main__':
    
    search_space_rv = init_search_space()
    
    with open('search_space_dict.pickle', 'wb') as handle:
        pickle.dump(search_space_rv, handle, protocol=pickle.HIGHEST_PROTOCOL)