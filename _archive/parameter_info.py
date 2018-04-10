#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:54:50 2018

@author: hildeweerts
"""

"""
Generate parameter info csv.
"""

import pandas as pd
import os
os.chdir('/Users/hildeweerts/hyperimp/')

# parameter settings Jan's experiment 
#alg_params = {'svm': ['gamma','C','tol','coef0'],
#              'svm_rbf': ['gamma','C','tol'],
#              'svm_sigmoid': ['gamma','C','tol','coef0'],
#              'rf': ['max_features','min_samples_leaf','min_samples_split'],
#              'ada': ['learning_rate','max_depth','n_estimators']}

# parameter settings experiment_1
alg_params = {'svm': ['gamma','C','tol', 'shrinking'],
              'rf': ['max_features','min_samples_leaf','min_samples_split', 'criterion', 'bootstrap']
              }

# parameters defined on a log scale
#logs = ['gamma', 'C', 'tol', 'learning_rate']
logs = ['gamma', 'C', 'tol']

# parameters defined on an integer scale
#integers = ['min_samples_leaf', 'min_samples_split', 'max_depth', 'n_estimators']
integers = ['min_samples_leaf', 'min_samples_split', 'max_depth']

# nominal parameters
nominals = ['criterion']

# boolean parameters
bools = ['bootstrap', 'shrinking']

alg_names = []
param_names = []
log_values = []
intg_values = []
nom_values = []
bool_values = []

for key, value in alg_params.items():
    for i in value:
        alg_names.append(key)
        param_names.append(i)
        log_values.append(i in logs)
        intg_values.append(i in integers)
        nom_values.append(i in nominals)
        bool_values.append(i in bools)
        
parameters = pd.DataFrame({'alg': alg_names,
                           'param_name': param_names,
                           'log': log_values,
                           'intg': intg_values,
                           'nom': nom_values,
                           'bool': bool_values})

parameters.to_csv('hyperimp/evaluate/parameters.csv', index = False)