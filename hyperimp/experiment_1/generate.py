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
import scipy
import random
import pandas as pd 
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

def generate_classifiers(algorithm, task_id, num):
    """
    Generate a list of classifiers.
    
    Parameters
    ----------
    algorithm : string with algorithm name
    task_id : integer, will be used as random seed
    num : integer, number of classifiers that will be generated
    """
    # get parameter dict for this classifier
    search_space = init_search_space()[algorithm]
    seed = task_id # use task_id as random seed to generate settings
    random.seed(seed)
    
    # generate num parameter settings
    param_settings = {}
    for param, domain in search_space.items():
        if isinstance(domain, list):
            samples = random.choices(domain, k = num)
        elif isinstance(domain, scipy.stats._distn_infrastructure.rv_frozen):
            samples = domain.rvs(size = num, random_state = seed)
        else:
            raise ValueError('Domain of %s is not properly specified.' % param)
        param_settings[param] = samples
    
    # create list of num classifiers
    classifiers = []
    
    for setting in pd.DataFrame(param_settings).to_dict('records'):
        if algorithm == 'random_forest':
            clf = RandomForestClassifier()
        elif algorithm == 'svm':
            clf = SVC()
        else:
            raise ValueError('Algorithm %s is misspelled or not implemented.' %s)
        clf.set_params(**setting)
        classifiers.append(clf)
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