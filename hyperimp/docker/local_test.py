#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:11:30 2018

@author: hildeweerts
"""
import os 
import openml
import requests
import numpy as np
from scipy.stats import uniform
from scipy.stats import randint
import sklearn
from sklearn import feature_selection

def tag_run(run_id, study_id, api_key):
    """ 
    Add run to study by tagging.
    
    Parameters
    ----------
    run_id : id of run to be added to study
    study_id: id of study to which run should be added
    api_key : openml api key necessary to communicate with openml api
    """
    tag = 'study_' + str(study_id)
    data = {'run_id': run_id,
            'tag': tag,
            'api_key': api_key}
    response = requests.post("https://www.openml.org/api/v1/json/run/tag", data = data).json()
    try:
        response['run_tag'] # check for errors
    except KeyError:
        print('Error %s : %s' %(response['error']['code'], response['error']['message']))
    return response

def build_rs(classifier, param_grid, indices, cv, n_iter):
    """ 
    Generate RandomSearchCV instance of classifier including simple preprocessing
    pipeline.
    
    Scaling is only used for SVM (i.e. it is removed for Random Forest or AdaBoost). 
    
    Parameters
    ----------
    classifier : sklearn classification object
    param_grid : parametergrid of classifier in the format {'clf__*hyperparameter* : distribution/list'}
    indices : list of indices of all categorical features in the dataset
    cv : number of folds in cross validation in a K-fold of Random Search
    n_iter : number of parameter samples that are sampled for the random search
    """
    steps = [('imputation', sklearn.preprocessing.Imputer(strategy='median')),
          ('hotencoding', sklearn.preprocessing.OneHotEncoder(handle_unknown='ignore', categorical_features=indices)),
          ('scaling', sklearn.preprocessing.StandardScaler(with_mean=False)),
          ('variencethreshold', sklearn.feature_selection.VarianceThreshold()),
          ('clf', classifier)]
    if isinstance(classifier, sklearn.ensemble.RandomForestClassifier) or isinstance(classifier, sklearn.ensemble.AdaBoostClassifier):
        del steps[2] 
    pipeline = sklearn.pipeline.Pipeline(steps = steps)
    model = sklearn.model_selection.RandomizedSearchCV(pipeline, param_grid, cv = cv, n_iter = n_iter)
    return model

def build_paramgrid(classifier, fixed_param):
    """
    Build sklearn classifier instance and parameter grid.
    
    Parameters
    ----------
    
    """
    return classifier, param_grid

def generate_models():
    """
    Generate all models that need to be evaluated. 
    """
    return models
#%%
# INPUT
task_id = 3
study_id = 98
api_key = '1b4da777588c6822623d44d9767d6225'
#%%

""" Sketch of main """
openml.config.apikey = os.environ.get('OPENMLKEY', api_key)# set OpenML API key to upload run
task = openml.tasks.get_task(task_id) # download openml task
indices = task.get_dataset().get_features_by_type('nominal', [task.target_name]) # find categorical instances
#%%
models = generate_models(....)
for model in models:
    run = openml.runs.run_model_on_task(task, model)
    run.publish()
    print("Uploaded to http://www.openml.org/r/" + str(run.run_id))
    tag_run(run.run_id, study_id, api_key)
    
#%%
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

classifier = SVC()
parma_grid = {'clf__gamma' : np.exp(uniform(-15, 3 - - 15))}
#%%
classifier = RandomForestClassifier()
param_grid = {'clf__bootstrap' : [True, False],
              #'clf__max_features' : np.random.uniform(0.1, 0.9),
              'clf__max_features' : uniform(loc = 0.1, scale = 0.9 - 0.1),
              'clf__min_samples_leaf' : randint(low = 1, high = 20),
              'clf__min_samples_split': randint(low = 2, high = 20)}
model = build_rs(classifier, param_grid, indices, 3, 10)
run = openml.runs.run_model_on_task(task, model)
#%%
run.fold_evaluations