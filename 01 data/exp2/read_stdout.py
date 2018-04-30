#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:31:19 2018

@author: hildeweerts
"""
"""
--------------------------------------------------------
Retrieve run_ids and experiment details from batch-labs
--------------------------------------------------------
"""

import os
import pandas as pd
import openml 
import pickle

# read uploaded and started
stdouts = []
#for root, dirs, files in os.walk('/Users/hildeweerts/hyperimp/01 data/exp2/batch-labs-2/'):
for root, dirs, files in os.walk('/Users/hildeweerts/Downloads/batch-labs'):
    for file in files:
        if file == 'stdout.txt':
            filepath = root + '/' + file
            with open(filepath) as f:
                txt = [l.strip() for l in f if 'Started' in l or 'Uploaded' in l or 'SCORE' in l]
                if len(txt) > 1:
                    stdouts.append(txt)

# read settings to dictionary
settings_list = []
for stdout in stdouts:
    settings = {}
    started = stdout[0].split()
    for setting in ['classifier', 'condition', 'parameter', 'deftype', 'seed', 'task']:
        i = started.index(setting)
        settings[setting] = started[i+1].replace("'", '').replace(',', '')
    #settings['acc_2f'] = float(stdout[1].split()[-1][:-1])
    uploaded = stdout[2].split()
    settings['run_id'] = uploaded[uploaded.index('id') + 1].replace('.', '')
    settings_list.append(settings)

# read manually added settings that were lost from batch-labs
settings_list_found = [
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'tol', 
         'seed' : '6', 'task' : '125922', 'run_id' : '9197702'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'shrinking', 
         'seed' : '8', 'task' : '146818', 'run_id' : '9196486'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'C', 
         'seed' : '6', 'task' : '14952', 'run_id' : '9196136'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'tol', 
         'seed' : '10', 'task' : '14954', 'run_id' : '9199020'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'shrinking', 
         'seed' : '3', 'task' : '167141', 'run_id' : '9194679'},
        {'classifier': 'svm', 'condition' : 'non-fixed', 
         'deftype' : 'None', 'parameter' : 'None', 
         'seed' : '3', 'task' : '18', 'run_id' : '9195209'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'criterion', 
         'seed' : '6', 'task' : '22', 'run_id' : '9197377'},
        {'classifier': 'random_forest', 'condition' : 'non-fixed', 
         'deftype' : 'None', 'parameter' : 'None', 
         'seed' : '4', 'task' : '23', 'run_id' : '9195201'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'max_features', 
         'seed' : '6', 'task' : '3021', 'run_id' : '9195822'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'gamma', 
         'seed' : '8', 'task' : '3913', 'run_id' : '9197442'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'bootstrap', 
         'seed' : '5', 'task' : '3918', 'run_id' : '9194538'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'bootstrap', 
         'seed' : '7', 'task' : '53', 'run_id' : '9197454'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'sklearn', 'parameter' : 'gamma', 
         'seed' : '3', 'task' : '6', 'run_id' : '9194334'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'C', 
         'seed' : '6', 'task' : '9910', 'run_id' : '9198889'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'tol', 
         'seed' : '9', 'task' : '9952', 'run_id' : '9197662'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'criterion', 
         'seed' : '6', 'task' : '9960', 'run_id' : '9197606'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'C', 
         'seed' : '4', 'task' : '9985', 'run_id' : '9194741'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'bootstrap', 
         'seed' : '6', 'task' : '125920', 'run_id' : '9195782'},
        {'classifier': 'random_forest', 'condition' : 'non-fixed', 
         'deftype' : 'None', 'parameter' : 'None', 
         'seed' : '7', 'task' : '125920', 'run_id' : '9196539'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'criterion', 
         'seed' : '9', 'task' : '146817', 'run_id' : '9196251'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'sklearn', 'parameter' : 'gamma', 
         'seed' : '5', 'task' : '146817', 'run_id' : '9195228'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'max_features', 
         'seed' : '10', 'task' : '146822', 'run_id' : '9199016'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'tol', 
         'seed' : '6', 'task' : '146822', 'run_id' : '9197628'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'bootstrap', 
         'seed' : '4', 'task' : '146824', 'run_id' : '9195064'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'max_features', 
         'seed' : '4', 'task' : '146824', 'run_id' : '9194651'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'max_features', 
         'seed' : '8', 'task' : '146824', 'run_id' : '9198933'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'min_samples_leaf', 
         'seed' : '5', 'task' : '2074', 'run_id' : '9194426'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'min_samples_split', 
         'seed' : '3', 'task' : '2074', 'run_id' : '9195322'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'shrinking', 
         'seed' : '4', 'task' : '2074', 'run_id' : '9194496'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'tol', 
         'seed' : '3', 'task' : '2074', 'run_id' : '9195112'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'criterion', 
         'seed' : '3', 'task' : '28', 'run_id' : '9195189'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'max_features', 
         'seed' : '7', 'task' : '28', 'run_id' : '9196010'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'gamma', 
         'seed' : '4', 'task' : '28', 'run_id' : '9194443'},
        {'classifier': 'svm', 'condition' : 'non-fixed', 
         'deftype' : 'None', 'parameter' : 'None', 
         'seed' : '3', 'task' : '28', 'run_id' : '9194968'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'bootstrap', 
         'seed' : '4', 'task' : '3022', 'run_id' : '9194572'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'sklearn', 'parameter' : 'max_features', 
         'seed' : '5', 'task' : '3022', 'run_id' : '9194519'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'C', 
         'seed' : '7', 'task' : '3022', 'run_id' : '9196482'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'sklearn', 'parameter' : 'gamma', 
         'seed' : '4', 'task' : '3022', 'run_id' : '9194167'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'min_samples_leaf', 
         'seed' : '6', 'task' : '32', 'run_id' : '9195944'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'min_samples_split', 
         'seed' : '3', 'task' : '32', 'run_id' : '9194816'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'tol', 
         'seed' : '8', 'task' : '32', 'run_id' : '9197441'},
        {'classifier': 'random_forest', 'condition' : 'non-fixed', 
         'deftype' : 'None', 'parameter' : 'None', 
         'seed' : '8', 'task' : '3549', 'run_id' : '9197620'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'gamma', 
         'seed' : '5', 'task' : '3549', 'run_id' : '9194743'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'bootstrap', 
         'seed' : '4', 'task' : '3560', 'run_id' : '9194348'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'tol', 
         'seed' : '5', 'task' : '3560', 'run_id' : '9194501'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'bootstrap', 
         'seed' : '3', 'task' : '3903', 'run_id' : '9194614'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'gamma', 
         'seed' : '4', 'task' : '3903', 'run_id' : '9194818'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'min_samples_leaf', 
         'seed' : '9', 'task' : '3904', 'run_id' : '9196771'},
        {'classifier': 'svm', 'condition' : 'non-fixed', 
         'deftype' : 'None', 'parameter' : 'None', 
         'seed' : '3', 'task' : '43', 'run_id' : '9194471'},
        {'classifier': 'svm', 'condition' : 'non-fixed', 
         'deftype' : 'None', 'parameter' : 'None', 
         'seed' : '4', 'task' : '43', 'run_id' : '9194986'},
        {'classifier': 'svm', 'condition' : 'non-fixed', 
         'deftype' : 'None', 'parameter' : 'None', 
         'seed' : '5', 'task' : '43', 'run_id' : '9195081'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'min_samples_leaf', 
         'seed' : '3', 'task' : '45', 'run_id' : '9194939'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'gamma', 
         'seed' : '3', 'task' : '45', 'run_id' : '9194863'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'hyperimp', 'parameter' : 'max_features', 
         'seed' : '7', 'task' : '9964', 'run_id' : '9197401'},
        {'classifier': 'random_forest', 'condition' : 'non-fixed', 
         'deftype' : 'None', 'parameter' : 'None', 
         'seed' : '7', 'task' : '9964', 'run_id' : '9196532'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'sklearn', 'parameter' : 'max_features', 
         'seed' : '7', 'task' : '9971', 'run_id' : '9198951'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'shrinking', 
         'seed' : '8', 'task' : '9971', 'run_id' : '9197630'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'min_samples_split', 
         'seed' : '5', 'task' : '9976', 'run_id' : '9195760'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'shrinking', 
         'seed' : '10', 'task' : '9976', 'run_id' : '9196927'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'sklearn', 'parameter' : 'gamma', 
         'seed' : '7', 'task' : '9976', 'run_id' : '9196476'},
        {'classifier': 'random_forest', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'min_samples_split', 
         'seed' : '7', 'task' : '9981', 'run_id' : '9197682'},
        {'classifier': 'svm', 'condition' : 'fixed', 
         'deftype' : 'None', 'parameter' : 'tol', 
         'seed' : '3', 'task' : '9981', 'run_id' : '9195223'}]
settings_list = settings_list + settings_list_found
runs_retrieved = list(set(pd.DataFrame(settings_list)['run_id']))
#%%
"""
--------------------------------------------------------
Retrieve accuracy scores from OpenML
--------------------------------------------------------
"""
for settings in settings_list:
    run_id = int(settings['run_id'])
    print(run_id)
    while True:
        try:
            run = openml.runs.get_run(run_id)
            break
        except openml.exceptions.OpenMLServerError as e:
            sleep(5)
    if len(run.evaluations) > 0:
        score = run.evaluations['predictive_accuracy']
    else:
        print("Run %s is not yet evaluated." % run_id )
        score = None
    settings['acc_openml'] = score

settings_df = pd.DataFrame(settings_list)
#%%
"""
--------------------------------------------------------
Save as pickle
--------------------------------------------------------
"""
with open('acc_data.pickle', 'wb') as handle:
    pickle.dump(settings_df, handle, protocol=pickle.HIGHEST_PROTOCOL)