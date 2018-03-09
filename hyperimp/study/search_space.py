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
    search_space = {
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
                'type' : 'exp',
                'min' : 0, # n ** 0
                'max' : 1}, # n ** 1
                
        ('random_forest', 'min_samples_leaf') : {
                'type' : 'int',
                'min' : 1,
                'max' : 20},
                
        ('random_forest', 'min_samples_split') : {
                'type' : 'int',
                'min' : 2,
                'max' : 20},
        
        ('adaboost', 'algorithm') : {
                'type' : 'nom',
                'domain' : ['SAMME', 'SAMME.R']},
        
        ('adaboost', 'learning_rate') : {
                'type' : 'log2',
                'min' : 0.01, 
                'max' : 2}, 

        ('adaboost', 'max_depth') : {
                'type' : 'int',
                'min' : 1,
                'max' : 10},
                
        ('adaboost', 'iterations') : {
                'type' : 'int',
                'min' : 50,
                'max' : 500},      
        }
        
    # Initialize loguniform objects
    loguniform = loguniform_gen(name='loguniform')
    loguniform_int = loguniform_int_gen(name = 'loguniform_int')
    
    search_space_rv = {}
    for (alg, param_name), param in search_space.items():
        print('Adding %s to dictionary...' %param_name)
        if param['type'] == 'int':
            rv = randint(low = param['min'], high = param['max'] + 1)
        elif param['type'] == 'log2': 
            rv = loguniform(base = 2, low = param['min'], high = param['max'])
        elif param['type'] == 'log10':
            rv = loguniform(base = 10, low = param['min'], high = param['max'])
        elif param['type'] == 'lin':
            rv = uniform(loc = param['min'], scale = param['max'] - param['min'])
        elif param['type'] == 'nom':
            rv = param['domain']
        elif param['type'] == 'exp':
            print("\tWarning: type 'exp' is not implemented yet.")
            #raise NotImplementedError()
        else:
            raise ValueError()
        search_space_rv[(alg, param_name)] = rv
        
    return search_space_rv

if __name__ == '__main__':
    
    search_space_rv = init_search_space()
    
    with open('data/search_space_rv.pickle', 'wb') as handle:
        pickle.dump(search_space_rv, handle, protocol=pickle.HIGHEST_PROTOCOL)