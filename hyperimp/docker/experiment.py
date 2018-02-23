#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:46:29 2018

@author: hildeweerts
"""

import argparse
import openml as oml
import sklearn
import requests


def parse_args():
    parser.add_argument("--seed", default=12345, type=int, help="random seed")
    parser = argparse.ArgumentParser(description='perform experiment')
    parser.add_argument('--openml_apikey', type=str, default=None, help='the apikey to authenticate to OpenML')
    parser.add_argument('--task_id', type=int, default=None, help='the openml task id')
    parser.add_argument('--study_id', type=str, default=98, help='the study to upload the runs to')
    parser.add_argument('--directory', type=str, default=None, help='the directory where the classifiers are stored')
    args = parser.parse_args()
    return args

def tag_run(run_id, study_id, api_key):
    """ 
    Add run to study
    
    Parameters
    ----------
    run_id : id of run to be added to study
    study_id: id of study to which task should be added
    api_key : openml api key necessary to communicate with openml api
    """
    
    tag = 'study_' + str(study_id)
    data = {'run_id': run_id,
            'tag': tag,
            'api_key': api_key}
    response = requests.post("https://www.openml.org/api/v1/json/task/tag", data = data).json()
    return response
    

if __name__ == '__main__':
    args = parse_args()
    task = openml.tasks.get_task(args.task_id) # download openml task
    oml.config.apikey = args.openml_apikey # set openml api key to upload run
    
    for clf in clfs:
        run = openml.runs.run_model_on_task(task, clf) # run classifier
        score = run.get_metric_score(sklearn.metrics.accuracy_score) # print accuracy score
        print('Data set: %s; Accuracy: %0.2f' % (task.get_dataset().name,score.mean()))
        run.publish() # publish the experiment on OpenML
        tag_run(run.run_id, args.study_id, args.openml_apikey) # tag experiment on OpenML