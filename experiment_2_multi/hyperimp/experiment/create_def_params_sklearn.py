#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 14:27:47 2018

@author: hildeweerts
"""

import pickle
    
def_params_sklearn = {
        'random_forest': {
                'max_features' : 'auto' ,
                'min_samples_leaf' : 1,
                'min_samples_split': 2, 
                'criterion' : 'gini',
                'bootstrap' : True},
        'svm': {'gamma': 'auto',
                'C' : 1.0 ,
                'tol' : 1e-3,
                'shrinking' : True
                } 
        }

with open('def_params_sklearn.pickle', 'wb') as handle:
    pickle.dump(def_params_sklearn, handle, protocol=pickle.HIGHEST_PROTOCOL)