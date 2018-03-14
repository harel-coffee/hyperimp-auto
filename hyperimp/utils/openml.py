#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 16:35:12 2018

@author: hildeweerts
"""

"""
Functions to deal with openml stuff.
"""

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