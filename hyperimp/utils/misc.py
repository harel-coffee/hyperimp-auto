#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 16:40:39 2018

@author: hildeweerts
"""

from time import gmtime, strftime

#by @janvanrijn
def get_time():
    return strftime("[%Y-%m-%d %H:%M:%S]", gmtime())