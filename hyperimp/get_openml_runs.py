#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 15:43:06 2018

@author: hildeweerts
"""
#%%
import openml
import sklearn
import pandas as pd

benchmark_suite = openml.study.get_study('OpenML-CC18','tasks') # obtain tasks of benchmark suite

# get all flows that contain the sklearn RandomForestClassifier that are not in a Voting
flows = openml.flows.list_flows()
rf_flows = []
rf_flows_descriptions = []
for flow_id, flow in flows.items():
    if 'sklearn.ensemble.forest.RandomForestClassifier' in flow['name'] and not 'VotingClassifier' in flow['name']:
        rf_flows.append(flow_id)
        rf_flows_descriptions.append(flow['name'])

# get all runs in benchmarksuite that are associated with a RandomForestClassifier flow
rf_runs = []
for task in benchmark_suite.tasks:
    end = False
    i = 0
    print('Currently processing task %i...' % task)
    # iterate over pages of task
    while not end:
        runs = openml.runs.list_runs(task=[task], offset = i*10000, size = 10000)
        i += 1
        print(i)
        for run_id, run_data in runs.items():
            # check if run is a random forest run
            if run_data['flow_id'] in rf_flows:
                rf_runs.append(run_id)
        if len(runs) < 10000:
            end = True        
            
# save run id's
pd.DataFrame(rf_runs).to_csv('rf_runs_2.csv')
