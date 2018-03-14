#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 10:30:22 2018

@author: hildeweerts
"""
#%%
import openml
import requests

def tag(object_id, object_type, study_id, api_key):
    """ add task, data, or run to a study
    
    Parameters
    ----------
    object_id : id of task/data/run to be added to study
    object_type : choose from 'task', 'data', 'run'
    study_id : id of study to which item should be added
    api_key : openml api key necessary to communicate with openml
    """
    tag = 'study_' + str(study_id)
    data = {object_type + '_id': object_id,
            'tag': tag,
            'api_key': api_key}
    response = requests.post("https://www.openml.org/api/v1/json/" + object_type + "/tag", data = data).json()
    return response

def untag(object_id, object_type, study_id, api_key):
    """ remove task, data, or run from a study
    
    Parameters
    ----------
    object_id : id of task/data/run to be removed from study
    object_type : choose from 'task', 'data', 'run'
    study_id : id of study from which object should be removed
    api_key : openml api key necessary to communicate with openml
    """
    tag = 'study_' + str(study_id)
    data = {object_type + '_id': object_id,
            'tag': tag,
            'api_key': api_key}
    response = requests.post("https://www.openml.org/api/v1/json/" + object_type + "/untag", data = data).json()
    return response

#%%
# remove all tasks and datasets from OpenML100 benchmark study
benchmark_suite = openml.study.get_study('OpenML100','tasks') # obtain the benchmark suite
api_key = 'b9398f7994a9f426ec19a122ef61b098'
study_id = 98

for task_id in benchmark_suite.tasks:
    task = openml.tasks.get_task(task_id)
    print('Untag task...')
    print(untag(task_id, 'task', study_id, api_key))
    print('Untag dataset...')
    dataset_id = task.dataset_id
    print(untag(dataset_id, 'data', study_id, api_key))
    
# add all tasks and datasets from openml CC18 benchmark study
benchmark_suite = openml.study.get_study('OpenML-CC18','tasks') # obtain the benchmark suite
api_key = 'b9398f7994a9f426ec19a122ef61b098'
study_id = 98

for task_id in benchmark_suite.tasks:
    task = openml.tasks.get_task(task_id)
    print('Tag task...')
    print(tag(task_id, 'task', study_id, api_key))
    print('Tag dataset...')
    dataset_id = task.dataset_id
    print(tag(dataset_id, 'data', study_id, api_key))