#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 11:52:41 2018

@author: hildeweerts
"""
import os
import pickle
import openml
import hyperimp.evaluate.importance as hyperimp

with open(os.getcwd() + '/01 data/exp2/acc_data.pickle', 'rb') as handle:
     data = pickle.load(handle)

traces = {}
i = 0
for run_id in data['run_id']:
    print(i)
    try:
        trace = openml.runs.get_run_trace(int(run_id))
        val_scores = hyperimp.get_val_scores(trace)
        traces[run_id] = val_scores
    except openml.exceptions.OpenMLServerException as e:
        print("Error in run %s: %s" % (run_id, e))
    i += 1

#%%
with open(os.getcwd() + '/01 data/exp2/trace_data_3.pickle', 'wb') as handle:
    pickle.dump(traces, handle, protocol=pickle.HIGHEST_PROTOCOL)
#%%