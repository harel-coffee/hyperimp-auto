#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 16:02:45 2018

@author: hildeweerts
"""
import os
import argparse
import openml
import hyperimp
import traceback
import sklearn
from joblib import Parallel, delayed
import arff
import pickle
from random import randint
from time import sleep
import pandas as pd
def parse_args():
    parser = argparse.ArgumentParser(description='Importance of Tuning')
    parser.add_argument('--study_id', type=int, default=98, help='the study id to retrieve tasks from')
    parser.add_argument('--task_ids', nargs = '*', type=int, default=[12], help='a list of tasks, leave None if a study is preferred')
    parser.add_argument('--classifier', type=str, default='svm', help='classifier that must be trained')
    parser.add_argument('--openml_apikey', type=str, default=None, help='the apikey to authenticate to OpenML')
    parser.add_argument('--num', type=int, default=1000, help='number of runs')
    parser.add_argument('--output_dir', type=str, default=os.path.expanduser('~') + '/results')
    parser.add_argument('--log', default=False, type=lambda x: (str(x).lower() == 'true'), help='results must be logged in container (True) or not (False)')
    return parser.parse_args()

@hyperimp.utils.misc.with_timeout(3*60*60)
def train_model(task, classifier):
    run = openml.runs.run_model_on_task(task, classifier)
    return run

def run_experiment(classifier, i, task_id, task, args):
    try:
        count = 1
        while count <= 100:
            try:
                print("%s Started run %d on task %s, dataset '%s'." % (hyperimp.utils.get_time(), i, task_id, task.get_dataset().name))
                # train model
                run = train_model(task, classifier)
                break
            except openml.exceptions.OpenMLServerError as e:
                if count == 100:
                    print("%s OpenMLServerError in run %d, I tried this 100 times already, so I'm just going to continue to the next run." % (hyperimp.utils.get_time(), i))
                    raise
                sleeptime = randint(5,60)
                print("%s Error in run %d, trying again in %d seconds. Message: %s" % (hyperimp.utils.get_time(), i, sleeptime, e))
                count += 1
                sleep(sleeptime)
        run.tags.append('study_%s' %str(args.study_id))
        score = run.get_metric_fn(sklearn.metrics.accuracy_score)
        print('%s [SCORE] run %d on task %s; Accuracy: %0.2f.' % (hyperimp.utils.get_time(), i, task_id, score.mean()))
        
        if args.log:
            # log xml, predictions, settings 
            output_dir = args.output_dir + '/' + args.classifier + '/task_' + str(task_id) + '/' + str(i)
            os.makedirs(output_dir)
            run_xml = run._create_description_xml()
            
            predictions_arff = arff.dumps(run._generate_arff_dict())
            with open(output_dir + '/run.xml', 'w') as f:
                f.write(run_xml)
            with open(output_dir + '/predictions.arff', 'w') as f:
                f.write(predictions_arff)
            with open(output_dir + '/param_settings.pickle', 'wb') as handle:
                pickle.dump(classifier.get_params(), handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            None
            
        count_run = 1
        while count_run <= 100:
            try:
                # publish run on OpenML
                run.publish()
                break
            except openml.exceptions.OpenMLServerError as e:
                if count_run == 100:
                    print("%s OpenMLServerError in run %d, I tried uploading this 100 times already, so I'm just going to continue to the next run." % (hyperimp.utils.get_time(), i))
                    raise
                sleeptime_run = randint(5,60)
                print("%s Error in uploading run %d, trying again in %d seconds. Message: %s" % (hyperimp.utils.get_time(), i, sleeptime_run, e))
                count_run += 1
                sleep(sleeptime_run)
        print("%s Uploaded run %d with run id %d." % (hyperimp.utils.get_time(), i, run.run_id))
        
    except TimeoutError as e:
        print("%s Run %d timed out." % (hyperimp.utils.get_time(), i))
    except Exception as e:
        print("%s Error in run %d: %s" % (hyperimp.utils.get_time(), i, e))
        #traceback.print_exc()
    return

if __name__ == '__main__':
    args = parse_args()
    # configure openml
    if args.openml_apikey is not None:
        openml.config.apikey = args.openml_apikey
    if args.log:
        print("%s Results will be logged locally in %s." % (hyperimp.utils.get_time(), args.output_dir))
    else:
        print("%s Results will not be logged locally." % (hyperimp.utils.get_time()))

    print('%s Retrieving tasks...' % hyperimp.utils.get_time())

    # retrieve tasks; task_ids argument is preferred, if not provided use study_id instead
    if args.task_ids is not None:
        print('%s Tasks will be retrieved based on provided task ids.' % hyperimp.utils.get_time())
        tasks = args.task_ids
    else:
        print('%s Tasks will be retrieved based on study id %d.' % (hyperimp.utils.get_time(), args.study_id))
        tasks = openml.study.get_study(args.study_id,'tasks').tasks
    print('%s The following tasks were retrieved: %s.' % (hyperimp.utils.get_time(),tasks))
    
    for task_id in tasks:
        
        try:
            #download task
            counts_task = 1
            while counts_task <= 100:
                try:
                    # train model
                    task = openml.tasks.get_task(task_id) 
                    break
                except openml.exceptions.OpenMLServerError as e:
                    if count_task == 100:
                        print("%s OpenMLServerError downloading task %d, I tried this 100 times already, so I'm just going to continue to the next run." % (hyperimp.utils.get_time(), task_id))
                        raise
                    sleeptime_task = randint(5,60)
                    print("%s Error in task %d, trying again in %d seconds. Message: %s" % (hyperimp.utils.get_time(), task_id, sleeptime_task, e))
                    count_task += 1
                    sleep(sleeptime_task)
            print('%s Downloaded task %d.' % (hyperimp.utils.get_time(), task_id))
            
            # generate pipeline objects
            classifiers = hyperimp.experiment.generate.generate_classifiers(args.classifier, task_id, args.num)
            indices = task.get_dataset().get_features_by_type('nominal', [task.target_name])
            pipelines = [hyperimp.experiment.generate.build_pipeline(clf, indices) for clf in classifiers]
            print('%s Prepared pipelines.' % hyperimp.utils.get_time())
            
            # Run num pipelines and upload to OpenML
            Parallel(n_jobs = -1)(delayed(run_experiment)(pipeline, i, task_id, task, args) for 
                     pipeline, i in zip(pipelines, range(1, len(pipelines) + 1)))
            
        except Exception as e:
            print("%s Error in task %d: %s" % (hyperimp.utils.get_time(), task_id, e))
            #traceback.print_exc()
