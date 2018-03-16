#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 16:40:39 2018

@author: hildeweerts
"""

from time import gmtime, strftime
import signal
import multiprocessing
import functools

#by @janvanrijn
def get_time():
    return strftime("[%Y-%m-%d %H:%M:%S]", gmtime())

# timeout decorator for timeout of a task within Parallel
def with_timeout(timeout):
    def decorator(decorated):
        @functools.wraps(decorated)
        def inner(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(1)
            async_result = pool.apply_async(decorated, args, kwargs)
            try:
                return async_result.get(timeout)
            except multiprocessing.TimeoutError:
                raise TimeoutError()
                return
        return inner
    return decorator