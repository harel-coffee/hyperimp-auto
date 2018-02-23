#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 14:51:01 2018

@author: hildeweerts
"""

"""
Add and removes tags to tasks to add to or remove from OpenML study.
"""

import openml
import requests

def tag_task(task_id, study_id, api_key):
    """ add task to a study
    Parameters
    ----------
    task_id : id of task to be added to study
    study_id: id of study to which task should be added
    api_key : openml api key necessary to communicate with openml
    """
    
    tag = 'study_' + str(study_id)
    data = {'task_id': task_id,
            'tag': tag,
            'api_key': api_key}
    response = requests.post("https://www.openml.org/api/v1/json/task/tag", data = data).json()
    return response

def untag_task(task_id, study_id, api_key):
    """ remove task from a study
    Parameters
    ----------
    task_id : id of task to be removed from study
    study_id: id of study from which task should be removed
    api_key : openml api key necessary to communicate with openml
    """
    tag = 'study_' + str(study_id)
    data = {'task_id': task_id,
            'tag': tag,
            'api_key': api_key}
    response = requests.post("https://www.openml.org/api/v1/json/task/untag", data = data).json()
    return response

#%%
api_key = '1b4da777588c6822623d44d9767d6225'
study_id = 98

# remove all tasks in study
study = openml.study.get_study(study_id, type= 'tasks')
for task_id in study.tasks:
    response = untag_task(task_id, study_id, api_key)

# add all tasks from openml 100 benchmark study
benchmark_suite = openml.study.get_study('OpenML100','tasks') # obtain the benchmark suite
for task_id in benchmark_suite.tasks:
    response = tag_task(task_id, study_id, api_key)