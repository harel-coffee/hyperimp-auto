#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 09:52:43 2018

@author: hildeweerts
"""
import argparse
import openml
import sklearn
import requests

def parse_args():
    parser = argparse.ArgumentParser(description='perform experiment')
    parser.add_argument("--seed", default=12345, type=int, help="random seed")
    parser.add_argument('--api_key', type=str, default=None, help='the apikey to authenticate to OpenML')
    parser.add_argument('--task_id', type=int, default=None, help='the openml task id')
    parser.add_argument('--study_id', type=str, default=98, help='the study to upload the runs to')
    args = parser.parse_args()
    return args

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
    response = requests.post("https://www.openml.org/api/v1/json/task/tag", data = data).json()
    if .... :
        print('Error %s : %s' %(response['error']['code'], respone['error']['message']))
    else:
        print('Added run to  OpenML study.')    
    return

if __name__ == '__main__':
    args = parse_args()
    task = openml.tasks.get_task(args.task_id) # download openml task
    openml.config.apikey = args.api_key # set OpenML API key to upload run
    
    for clf in classifiers:
        run = openml.runs.run_model_on_task(task, clf) # run classifier
        print('Data set: %s; Accuracy: %0.2f' % (task.get_dataset().name,score.mean()))
        run.publish() # publish results on OpenML
        print("Uploaded to http://www.openml.org/r/" + str(myrun.run_id))
        tag_run(run.run_id, study_id, args.api_key) # tag run on OpenML