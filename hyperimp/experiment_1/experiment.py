#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 16:02:45 2018

@author: hildeweerts
"""
import argparse
import openml
import hyperimp

def parse_args():
    parser = argparse.ArgumentParser(description='Importance of Tuning')
    parser.add_argument('--cache_directory', type=str, default=os.path.expanduser('~') + '/experiments/active_testing',
                        help='directory to store cache')
    parser.add_argument('--task_id', type=int, default=None, help='limit number of tasks (for testing)')
    parser.add_argument('--study_id', type=int, default='98', help='the tag to obtain the tasks from')
    parser.add_argument('--classifier', type =str, default='random_forest', help='classifier that must be trained')
    parser.add_argument('--openml_apikey', type=str, default=None, help='the apikey to authenticate to OpenML')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    if args.task_id is None:
        raise ValueError('task_id not given')
    else:
        task_id = args.task_id
    
    task = openml.tasks.get_task(task_id) #download task
    print('%s Downloaded task %d' % (hyperimp.utils.get_time(), task_id))
    
    indices = task.get_dataset().get_features_by_type('nominal', [task.target_name])
    classifiers = generate_classifiers(args.algorithm)
    pipelines = [build_pipeline(clf, indices) for clf in classifiers]
    
    for classifier in classifiers:
        try:
            run = openml.runs.run_model_on_task(task, classifier)
            run.tags.append('study_%s' %str(study_id))
            score = run.get_metric_fn(sklearn.metrics.accuracy_score)
            print('%\t s [SCORE] Data: %s; Accuracy: %0.2f' % (hyperimp.utils.get_time(), task.get_dataset().name, score.mean()))
            run.publish()
            print("%\t s Uploaded with run id %d" % (hyperimp.utils.get_time(), run.run_id))
        except ValueError as e:
            traceback.print_exc()
        except TypeError as e:
            traceback.print_exc()
        except OpenMLServerException as e:
            traceback.print_exc()
        except Exception as e:
            traceback.print_exc()