#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 20:20:22 2018

@author: hildeweerts
"""

"""
Attempt to parallelize getting traces.
Does not work because kernel dies when trying to access np.memmap object #sadpanda
"""

import os
import pickle
import openml
import hyperimp.evaluate.importance as hyperimp
from joblib import Parallel, delayed
import numpy as np
import tempfile
import shutil

def get_trace(run_id, i, temp):
    print('%s : %s' %(i, run_id))
    try:
        temp[i] = hyperimp.get_val_scores(openml.runs.get_run_trace(int(run_id)))
    except openml.exceptions.OpenMLServerException as e:
            print("Error in run %s: %s" % (run_id, e)) 
    return

if __name__ == '__main__':
    with open(os.getcwd() + '/01 data/exp2/acc_data.pickle', 'rb') as handle:
        data = pickle.load(handle)
    
    data = data[0:20]
    
    # Creat a temporary directory and define the array path
    path = tempfile.mkdtemp()
    temppath = os.path.join(path,'temp.mmap')
    
    # Define variables
    run_ids = list(data['run_id'])
    
    # Create array using numpy's memmap
    temp = np.memmap(temppath, dtype = object, shape = (np.size(run_ids), 100), mode='w+')
    
    # parallel process 
    Parallel(n_jobs=-1)(delayed(get_trace)(run_id, i, temp) 
    for run_id, i in zip(data['run_id'], range(0, len(data))))
    
    # show array output
    print(temp)
    
    # Delete the temporary directory and contents
    try:
        shutil.rmtree(path)
    except:
        print("Couldn't delete folder: "+ str(path))
