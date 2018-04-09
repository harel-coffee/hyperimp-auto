#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 15:27:17 2018

@author: hildeweerts
"""

import openml

study_id = 98

# configure your apikey if you don't have config file
#apikey = 'apikey'
#openml.config.apikey = apikey

tasks = openml.study.get_study(study_id).tasks
for task_id in tasks:
    print("\t- '%d'" % task_id)