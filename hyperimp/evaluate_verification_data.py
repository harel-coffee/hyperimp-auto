#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:48:52 2018

@author: hildeweerts
"""
"""
Generate verificaiton_*classifier*.csv.

Compute accuracy of predictions of Jan's verification experiment and save the
scores in a csv with columns:
    accuracy, fold, fixed_param, fixed_value, dataset
"""
import os
import arff
import pandas as pd
from sklearn.metrics import accuracy_score

os.chdir('/Users/hildeweerts/desktop/TUe/Internship Columbia/02 Results Jan/rs_experiments/libsvm_svc/kernel_sigmoid')
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
    index = split.index('kernel_sigmoid')
    acc_scores['fixed_param'] = split[index + 1].replace('classifier__', '')
    acc_scores['fixed_value'] = split[index + 2]
    acc_scores['dataset'] = split[index + 3]
    
    # append accuracy score
    accuracy_scores = accuracy_scores.append(acc_scores)
    
    i += 1
    print(i)
    
#accuracy_scores.to_csv('svm_sigmoid.csv', index = False)
