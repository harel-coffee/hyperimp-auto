#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 16:02:45 2018

@author: hildeweerts
"""
import argparse
import openml
import hyperimp
import os
import traceback
import sklearn
from openml.exceptions import OpenMLServerException

def parse_args():
    parser = argparse.ArgumentParser(description='Importance of Tuning')
    parser.add_argument('--study_id', type=int, default=98, help='the study id to retrieve tasks from')
    parser.add_argument('--classifier', type=str, default='random_forest', help='classifier that must be trained')
    parser.add_argument('--openml_apikey', type=str, default=None, help='the apikey to authenticate to OpenML')
    parser.add_argument('--num', type=int, default=3, help='number of runs')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    # retrieve tasks_id's from study
    tasks = openml.study.get_study(args.study_id,'tasks').tasks
    
    for task_id in tasks:
        try:
            #download task
            task = openml.tasks.get_task(task_id) 
            print('%s Downloaded task %d' % (hyperimp.utils.get_time(), task_id))
            
            # generate pipeline objects
            classifiers = hyperimp.experiment_1.generate.generate_classifiers(args.classifier, task_id, args.num)
            indices = task.get_dataset().get_features_by_type('nominal', [task.target_name])
            pipelines = [hyperimp.experiment_1.generate.build_pipeline(clf, indices) for clf in classifiers]
            print('%s Prepared pipelines.' % hyperimp.utils.get_time())
            
            # Run num classifiers and upload to OpenML
            for classifier, i in zip(classifiers, range(1, len(classifiers) + 1 )):
                try: 
                    print("%s Started run %d on task %s, dataset '%s'" % (hyperimp.utils.get_time(), i, task_id, task.get_dataset().name))
                    run = openml.runs.run_model_on_task(task, classifier)
                    run.tags.append('study_%s' %str(args.study_id))
                    score = run.get_metric_fn(sklearn.metrics.accuracy_score)
                    print('%s [SCORE] run %d on task %s; Accuracy: %0.2f' % (hyperimp.utils.get_time(), i, task_id, score.mean()))
                    run.publish()
                    print("%s Uploaded with run id %d" % (hyperimp.utils.get_time(), run.run_id))
                except ValueError as e:
                    traceback.print_exc()
                except TypeError as e:
                    traceback.print_exc()
                except Exception as e:
                    traceback.print_exc()
                except OpenMLServerException as e:
                    traceback.print_exc()
        except ValueError as e:
            traceback.print_exc()
        except TypeError as e:
            traceback.print_exc()
        except Exception as e:
            traceback.print_exc()
        except OpenMLServerException as e:
            traceback.print_exc()