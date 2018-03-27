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

def parse_args():
    parser = argparse.ArgumentParser(description='Importance of Tuning')
    parser.add_argument('--study_id', type=int, default=98, help='the study id to retrieve tasks from')
    parser.add_argument('--classifier', type=str, default='random_forest', help='classifier that must be trained')
    parser.add_argument('--openml_apikey', type=str, default=None, help='the apikey to authenticate to OpenML')
    parser.add_argument('--num', type=int, default=5, help='number of runs')
    parser.add_argument('--output_dir', type=str, default=os.path.expanduser('~') + '/results')
    return parser.parse_args()

@hyperimp.utils.misc.with_timeout(40*60)
def train_model(task, classifier):
    run = openml.runs.run_model_on_task(task, classifier)
    return run

def run_experiment(classifier, i, task_id, task, args):
    try:
        # train model
        print("%s Started run %d on task %s, dataset '%s'." % (hyperimp.utils.get_time(), i, task_id, task.get_dataset().name))
        run = train_model(task, classifier)
        run.tags.append('study_%s' %str(args.study_id))
        score = run.get_metric_fn(sklearn.metrics.accuracy_score)
        print('%s [SCORE] run %d on task %s; Accuracy: %0.2f.' % (hyperimp.utils.get_time(), i, task_id, score.mean()))
        
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
            
        # publish run on OpenML
        run.publish()
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
    print('%s Retrieving tasks...' % hyperimp.utils.get_time())
    # retrieve tasks_id's from study
    tasks = openml.study.get_study(args.study_id,'tasks').tasks
    print('%s Tasks retrieved.' % hyperimp.utils.get_time())
    for task_id in tasks:
        try:
            #download task
            task = openml.tasks.get_task(task_id) 
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