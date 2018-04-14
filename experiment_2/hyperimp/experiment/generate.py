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
from hyperimp.utils.preprocessing import ConditionalImputer
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV

def build_pipeline(classifier, indices):
    """ 
    Build pipeline of classifier including simple preprocessing steps.
    
    Scaling is only used for SVM (i.e. it is removed for Random Forest or AdaBoost). 
    
    Parameters
    ----------
    classifier : sklearn classification object including parameter settings
    indices : list of indices of all categorical features in the dataset
    """
    steps = [('imputation', ConditionalImputer(fill_empty=0, 
                                               categorical_features=indices, 
                                               strategy = 'mean', 
                                               strategy_nominal='most_frequent')),
          ('hotencoding', sklearn.preprocessing.OneHotEncoder(handle_unknown='ignore', categorical_features=indices)),
          ('scaling', sklearn.preprocessing.StandardScaler(with_mean=False)),
          ('variencethreshold', sklearn.feature_selection.VarianceThreshold()),
          ('clf', classifier)]
    if isinstance(classifier, sklearn.ensemble.RandomForestClassifier) or isinstance(classifier, sklearn.ensemble.AdaBoostClassifier):
        del steps[2] 
    pipeline = sklearn.pipeline.Pipeline(steps = steps)
    return pipeline

def build_rscv(algorithm, indices, n_iter, seed, params):
    """
    Build random search cv object with 3-fold cv.
    
    parameters
    ----------
    algorithm : str
        random_forest or svm
    indices : list 
        indices of all categorical features in the dataset
    n_iter : int 
        number of iterations random search
    seed : int
        random search seed
    params : dict
        { clf__paramname : list/distribution }
    """
    # build pipeline
    if algorithm == 'random_forest':
        clf = RandomForestClassifier()
    elif algorithm == 'svm':
        clf = SVC()
    else:
        raise ValueError('Algorithm %s is misspelled or not implemented.' %algorithm)
    pipeline = build_pipeline(clf, indices)
    
    # build rscv
    rscv = RandomizedSearchCV(estimator=pipeline, param_distributions=params, 
                              n_iter=n_iter, fit_params=None, n_jobs=-1, 
                              refit=False, cv=3, random_state=seed)    
    return rscv

def build_params(param, fixed_value):
    """
    Generates dictionary that can be used in randomsearchcv.
    
    Parameters
    ----------
    param : str
        hyperparameter
    fixed : ...
        the fixed value of the hyperparameter (e.g. 'gini' or 1)
        set to None to NOT fix the parameter
    """
    params = ...
        key = 'clf__' + name 
        
    if fixed is not None:
        params[fixed] = fixed
    return params
