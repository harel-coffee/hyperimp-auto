#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 17:20:12 2018

@author: hildeweerts
"""

"""
Set of functions to build simple pipelines with hyperparametersettings randomly
taken from the search space.
"""

from hyperimp.study.search_space import init_search_space
import random

def generate_classifiers(algorithm, search_space, task_id, num):
    """
    Generate a list of classifiers.
    
    Parameters
    ----------
    algorithm : string with algorithm name
    search_space : dictionary generated through hyperimp.study.search_space.init_search_space()
    task_id : integer, will be used as random seed
    num : integer, number of classifiers that will be generated
    """
    # get parameter dict for this classifier
    search_space = init_search_space()[algorithm]
    random.seed(task_id)
    seeds 
    
    classifiers = []
    for i in range(num):
        # randomly pick values 
        
        # initiate classifier
        classifier = ...
        classifiers.append(classifier)
    
    return classifiers

def build_pipeline(classifier, indices):
    """ 
    Build pipeline of classifier including simple preprocessing steps.
    
    Scaling is only used for SVM (i.e. it is removed for Random Forest or AdaBoost). 
    
    Parameters
    ----------
    classifier : sklearn classification object including parameter settings
    indices : list of indices of all categorical features in the dataset
    """
    steps = [('imputation', sklearn.preprocessing.Imputer(strategy='mean')),
          ('hotencoding', sklearn.preprocessing.OneHotEncoder(handle_unknown='ignore', categorical_features=indices)),
          ('scaling', sklearn.preprocessing.StandardScaler(with_mean=False)),
          ('variencethreshold', sklearn.feature_selection.VarianceThreshold()),
          ('clf', classifier)]
    if isinstance(classifier, sklearn.ensemble.RandomForestClassifier) or isinstance(classifier, sklearn.ensemble.AdaBoostClassifier):
        del steps[2] 
    pipeline = sklearn.pipeline.Pipeline(steps = steps)
    return pipeline