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
import arff
import pickle
from random import randint
from time import sleep

def parse_args():
    parser = argparse.ArgumentParser(description='Importance of Tuning')
    parser.add_argument('--study_id', type=int, default=98, help='OpenML study id')
    parser.add_argument('--task_id', type=int, default=18, help='OpenML task id')
    parser.add_argument('--param', type=str, default='max_features', help='Hyperparameter of interest.')
    parser.add_argument('--seed', type=str, default=1, help='Seed of the random search.')
    parser.add_argument('--condition', type=str, default='non-fixed', help="fixed' or 'non-fixed' experiment.")
    parser.add_argument('--n_iter', type=int, default=100, help='Number of iterations of the random search.')
    parser.add_argument('--classifier', type=str, default='random_forest', help='classifier that must be trained')
    parser.add_argument('--openml_apikey', type=str, default=None, help='the apikey to authenticate to OpenML')
    parser.add_argument('--output_dir', type=str, default=os.path.expanduser('~') + '/results')
    parser.add_argument('--log', default=False, type=lambda x: (str(x).lower() == 'true'), help='results must be logged in container (True) or not (False)')
    return parser.parse_args()

@hyperimp.utils.misc.with_timeout(3*60*60)
def train_model(task, classifier):
    run = openml.runs.run_model_on_task(task, classifier)
    return run

def run_experiment(rscv, task, args):
    try: 
        count = 1
        while count <= 100:
            try:
                print("%s Started condition %s, parameter %s, RS seed %d on task %s, dataset '%s'." % (hyperimp.utils.get_time(), args.condition, args.param, args.seed, args.task_id, task.get_dataset().name))
                # train model
                run = train_model(task, rscv)
                break
            except openml.exceptions.OpenMLServerError as e:
                if count == 100:
                    print("%s OpenMLServerError in run, I tried this 100 times already, so I'm just going to continue to the next run." % (hyperimp.utils.get_time()))
                    raise
                sleeptime = randint(5,60)
                print("%s Error in run, trying again in %d seconds. Message: %s" % (hyperimp.utils.get_time(), sleeptime, e))
                count += 1
                sleep(sleeptime)
        run.tags.append('study_%s' %str(args.study_id))
        score = run.get_metric_fn(sklearn.metrics.accuracy_score)
        print('%s [SCORE] Accuracy: %0.2f.' % (hyperimp.utils.get_time(), score.mean()))
        
        if args.log:
            # log xml, predictions 
            output_dir = args.output_dir + '/' + args.classifier + '/task_' + str(args.task_id) + '/' + str(args.condition)
            os.makedirs(output_dir)
            run_xml = run._create_description_xml()
            predictions_arff = arff.dumps(run._generate_arff_dict())
            with open(output_dir + '/run.xml', 'w') as f:
                f.write(run_xml)
            with open(output_dir + '/predictions.arff', 'w') as f:
                f.write(predictions_arff)
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
                    print("%s OpenMLServerError in run, I tried uploading this 100 times already, so I'm just going to continue to the next run." % (hyperimp.utils.get_time()))
                    raise
                sleeptime_run = randint(5,60)
                print("%s Error in uploading run trying again in %d seconds. Message: %s" % (hyperimp.utils.get_time(), sleeptime_run, e))
                count_run += 1
                sleep(sleeptime_run)
        print("%s Uploaded run with run id %d." % (hyperimp.utils.get_time(), run.run_id))
    except TimeoutError as e:
        print("%s Run timed out." % (hyperimp.utils.get_time()))
    except Exception as e:
        print("%s Error in run: %s" % (hyperimp.utils.get_time(), e))
        traceback.print_exc()
    return

if __name__ == '__main__':
    args = parse_args()
    print(os.getcwd())
    
    # configure openml
    if args.openml_apikey is not None:
        openml.config.apikey = args.openml_apikey
    if args.log:
        print("%s Results will be logged locally in %s." % (hyperimp.utils.get_time(), args.output_dir))
    else:
        print("%s Results will not be logged locally." % (hyperimp.utils.get_time()))

    print('%s Retrieving tasks...' % hyperimp.utils.get_time())
    
    try:
        #download task
        count_task = 1
        while count_task <= 100:
            try:
                # train model
                task = openml.tasks.get_task(args.task_id) 
                break
            except openml.exceptions.OpenMLServerError as e:
                if count_task == 100:
                    print("%s OpenMLServerError downloading task %d, I tried this 100 times already, so I'm just going to continue to the next run." % (hyperimp.utils.get_time(), args.task_id))
                    raise
                sleeptime_task = randint(5,60)
                print("%s Error in task %d, trying again in %d seconds. Message: %s" % (hyperimp.utils.get_time(), args.task_id, sleeptime_task, e))
                count_task += 1
                sleep(sleeptime_task)
        print('%s Downloaded task %d.' % (hyperimp.utils.get_time(), args.task_id))

        # build RandomizedSearchCV object
        search_space = hyperimp.study.search_space.init_search_space()[args.classifier]
        if args.condition == "fixed":
            # load default parameter setting
            with open('def_params.pickle', 'rb') as handle:
                def_params = pickle.load(handle)
            def_param = def_params[args.classifier][args.task_id][args.param]
            # retrieve parameter settings with param fixed to def_param
            params = hyperimp.experiment.generate.build_params(args.param, def_param, search_space)
        elif args.condition == "non-fixed":
            params = hyperimp.experiment.generate.build_params(args.param, None, search_space)
        else:
            raise ValueError("invalid 'condition' argument")
        indices = task.get_dataset().get_features_by_type('nominal', [task.target_name])
        rscv = hyperimp.experiment.generate.build_rscv(args.classifier, indices, args.n_iter, args.seed, params)

        # run experiment
        run_experiment(rscv, task, args)
        
    except Exception as e:
        print("%s Error in run: %s" % (hyperimp.utils.get_time(), e))
        traceback.print_exc()