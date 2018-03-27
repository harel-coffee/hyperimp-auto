#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:48:52 2018

@author: hildeweerts
"""

import os
import arff
import pandas as pd
from sklearn.metrics import accuracy_score

"""
Generate verification_*classifier*.csv.

Compute accuracy of predictions of Jan's verification experiment and save the
scores in a csv with columns:
    accuracy, fold, fixed_param, fixed_value, dataset
"""

os.chdir('/Users/hildeweerts/desktop/TUe/Internship Columbia/02 Results Jan/rs_experiments/random_forest/vanilla')
files = [os.path.join(r,file) for r,d,f in os.walk(os.getcwd()) for file in f if file.endswith('predictions.arff')]

accuracy_scores = pd.DataFrame()
i=0
for file in files:
    
    # read file
    with open(file, 'r') as fp:
            pred_arff = arff.load(fp)
    attributes = pred_arff['attributes']
    columns = [d[0] for d in attributes]
    df = pd.DataFrame(pred_arff['data'], columns = columns)
    
    # determine accuracy scores for the different folds
    folds = []
    scores = []
    for fold, group in df.groupby('fold'):
        folds.append(int(fold))
        scores.append(accuracy_score(group['prediction'], group['correct']))
    acc_scores = pd.DataFrame(data = [scores, folds]).transpose()
    acc_scores.columns = ['accuracy', 'fold']
    
    # add info dataset/fixed param info
    split = file.split('/')
    index = split.index('vanilla')
    acc_scores['fixed_param'] = split[index + 1].replace('classifier__', '')
    acc_scores['fixed_value'] = split[index + 2]
    acc_scores['dataset'] = split[index + 3]
    
    # append accuracy score
    accuracy_scores = accuracy_scores.append(acc_scores)
    
    i += 1
    print(i)
    
accuracy_scores.to_csv('verification__rf.csv', index = False)
    
#%%
"""
Generate rs_*classifier*.csv

Compute accuracy of predictions of Jan's random search experiment and save the
scores in a csv with columns:
    accuracy, fold, dataset, seed
"""
os.chdir('/Users/hildeweerts/desktop/TUe/Internship Columbia/02 Results Jan/random_search_50/random_forest/vanilla/uniform__bestN_10__ignore_logscale_False__inverse_holdout_False__oob_strategy_resample')
files = [os.path.join(r,file) for r,d,f in os.walk(os.getcwd()) for file in f if file.endswith('predictions.arff')]

accuracy_scores = pd.DataFrame()
i=0
for file in files:
    
    # read file
    with open(file, 'r') as fp:
            pred_arff = arff.load(fp)
    attributes = pred_arff['attributes']
    columns = [d[0] for d in attributes]
    df = pd.DataFrame(pred_arff['data'], columns = columns)
    
    # determine accuracy scores for the different folds
    folds = []
    scores = []
    for fold, group in df.groupby('fold'):
        folds.append(int(fold))
        scores.append(accuracy_score(group['prediction'], group['correct']))
    acc_scores = pd.DataFrame(data = [scores, folds]).transpose()
    acc_scores.columns = ['accuracy', 'fold']
    
    # add info dataset/fixed param info
    split = file.split('/')
    index = split.index('uniform__bestN_10__ignore_logscale_False__inverse_holdout_False__oob_strategy_resample')
    acc_scores['dataset'] = split[index + 1]
    acc_scores['seed'] = split[index + 2]
    # append accuracy score
    accuracy_scores = accuracy_scores.append(acc_scores)
    
    i += 1
    print(i)

accuracy_scores.to_csv('rs_rf.csv', index = False)