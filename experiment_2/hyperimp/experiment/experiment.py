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
import random
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description='Importance of Tuning')
    parser.add_argument('--study_id', type=int, default=98, help='OpenML study id, used for tagging.')
    parser.add_argument('--task_id', type=int, default=3, help='OpenML task id.')
    parser.add_argument('--param', type=str, default=None, help='Hyperparameter of interest.')
    parser.add_argument('--seed', type=int, default=1, help='Seed of the random search.')
    parser.add_argument('--condition', type=str, default='non-fixed', help="fixed' or 'non-fixed' experiment.")
    parser.add_argument('--n_iter', type=int, default=100, help='Number of iterations of the random search.')
    parser.add_argument('--cv', type=int, default=5, help='Number of cv folds in random search.')
    parser.add_argument('--classifier', type=str, default='random_forest', help='classifier that must be trained, choose from random_forest and svm')
    parser.add_argument('--openml_apikey', type=str, default=None, help='the apikey to authenticate to OpenML')
    parser.add_argument('--output_dir', type=str, default=os.path.expanduser('~') + '/results')
    parser.add_argument('--deftype', type = str, default=None, help="only used for max_features and gamma. Choose either 'sklearn' or 'hyperimp'")
    parser.add_argument('--log', default=False, type=lambda x: (str(x).lower() == 'true'), help='results must be logged in container (True) or not (False)')
    return parser.parse_args()

#@hyperimp.utils.misc.with_timeout(3*60*60)
def train_model(task, classifier):
    run = openml.runs.run_model_on_task(task, classifier)
    return run

def run_experiment(rscv, task, args):
    try: 
        count = 1
        while count <= 100:
            try:
                print("%s Started classifier %s, condition %s, parameter '%s', deftype '%s', RS seed %s on task %s, dataset '%s'." % (hyperimp.utils.get_time(), args.classifier, args.condition, args.param, args.deftype, args.seed, args.task_id, task.get_dataset().name))
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
        print("%s Uploaded run condition %s, parameter %s, RS seed %s, task %s, with run id %d." % (hyperimp.utils.get_time(), args.condition, args.param, args.seed, args.task_id, run.run_id))
    except TimeoutError as e:
        print("%s Run timed out." % (hyperimp.utils.get_time()))
    except Exception as e:
        print("%s Error in run: %s" % (hyperimp.utils.get_time(), e))
        traceback.print_exc()
    return

print(os.getcwd())
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# MONKEY PATCH FOR CONDITION == FIXED
import warnings
import numpy as np
from itertools import product
from collections import defaultdict
from scipy.stats import rankdata
from functools import partial

from sklearn.model_selection._split import check_cv
from sklearn.model_selection._validation import _fit_and_score
from sklearn.model_selection._validation import _aggregate_score_dicts
from sklearn.base import is_classifier, clone
from sklearn.metrics.scorer import _check_multimetric_scoring
from sklearn.externals.joblib import Parallel, delayed
from sklearn.externals import six
from sklearn.utils.validation import indexable
from sklearn.utils.deprecation import DeprecationDict
from sklearn.utils.fixes import MaskedArray

def fit(self, X, y=None, groups=None, **fit_params):
    """Run fit with all sets of parameters.
    Parameters
    ----------
    X : array-like, shape = [n_samples, n_features]
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.
    y : array-like, shape = [n_samples] or [n_samples, n_output], optional
        Target relative to X for classification or regression;
        None for unsupervised learning.
    groups : array-like, with shape (n_samples,), optional
        Group labels for the samples used while splitting the dataset into
        train/test set.
    **fit_params : dict of string -> object
        Parameters passed to the ``fit`` method of the estimator
    """
    if self.fit_params is not None:
        warnings.warn('"fit_params" as a constructor argument was '
                      'deprecated in version 0.19 and will be removed '
                      'in version 0.21. Pass fit parameters to the '
                      '"fit" method instead.', DeprecationWarning)
        if fit_params:
            warnings.warn('Ignoring fit_params passed as a constructor '
                          'argument in favor of keyword arguments to '
                          'the "fit" method.', RuntimeWarning)
        else:
            fit_params = self.fit_params
    estimator = self.estimator
    cv = check_cv(self.cv, y, classifier=is_classifier(estimator))

    scorers, self.multimetric_ = _check_multimetric_scoring(
        self.estimator, scoring=self.scoring)

    if self.multimetric_:
        if self.refit is not False and (
                not isinstance(self.refit, six.string_types) or
                # This will work for both dict / list (tuple)
                self.refit not in scorers):
            raise ValueError("For multi-metric scoring, the parameter "
                             "refit must be set to a scorer key "
                             "to refit an estimator with the best "
                             "parameter setting on the whole data and "
                             "make the best_* attributes "
                             "available for that metric. If this is not "
                             "needed, refit should be set to False "
                             "explicitly. %r was passed." % self.refit)
        else:
            refit_metric = self.refit
    else:
        refit_metric = 'score'

    X, y, groups = indexable(X, y, groups)
    n_splits = cv.get_n_splits(X, y, groups)
    # Regenerate parameter iterable for each fit
    candidate_params = list(self._get_param_iterator())
    
    # Monkey patch: alter parameter to fixed value
    if args.condition == 'fixed':
        for monkey_param in candidate_params:
            monkey_param['clf__' + args.param] = def_param

            
    n_candidates = len(candidate_params)
    if self.verbose > 0:
        print("Fitting {0} folds for each of {1} candidates, totalling"
              " {2} fits".format(n_splits, n_candidates,
                                 n_candidates * n_splits))

    base_estimator = clone(self.estimator)
    pre_dispatch = self.pre_dispatch

    out = Parallel(
        n_jobs=self.n_jobs, verbose=self.verbose,
        pre_dispatch=pre_dispatch
    )(delayed(_fit_and_score)(clone(base_estimator), X, y, scorers, train,
                              test, self.verbose, parameters,
                              fit_params=fit_params,
                              return_train_score=self.return_train_score,
                              return_n_test_samples=True,
                              return_times=True, return_parameters=False,
                              error_score=self.error_score)
      for parameters, (train, test) in product(candidate_params,
                                               cv.split(X, y, groups)))

    # if one choose to see train score, "out" will contain train score info
    if self.return_train_score:
        (train_score_dicts, test_score_dicts, test_sample_counts, fit_time,
         score_time) = zip(*out)
    else:
        (test_score_dicts, test_sample_counts, fit_time,
         score_time) = zip(*out)

    # test_score_dicts and train_score dicts are lists of dictionaries and
    # we make them into dict of lists
    test_scores = _aggregate_score_dicts(test_score_dicts)
    if self.return_train_score:
        train_scores = _aggregate_score_dicts(train_score_dicts)

    # TODO: replace by a dict in 0.21
    results = (DeprecationDict() if self.return_train_score == 'warn'
               else {})

    def _store(key_name, array, weights=None, splits=False, rank=False):
        """A small helper to store the scores/times to the cv_results_"""
        # When iterated first by splits, then by parameters
        # We want `array` to have `n_candidates` rows and `n_splits` cols.
        array = np.array(array, dtype=np.float64).reshape(n_candidates,
                                                          n_splits)
        if splits:
            for split_i in range(n_splits):
                # Uses closure to alter the results
                results["split%d_%s"
                        % (split_i, key_name)] = array[:, split_i]

        array_means = np.average(array, axis=1, weights=weights)
        results['mean_%s' % key_name] = array_means
        # Weighted std is not directly available in numpy
        array_stds = np.sqrt(np.average((array -
                                         array_means[:, np.newaxis]) ** 2,
                                        axis=1, weights=weights))
        results['std_%s' % key_name] = array_stds

        if rank:
            results["rank_%s" % key_name] = np.asarray(
                rankdata(-array_means, method='min'), dtype=np.int32)

    _store('fit_time', fit_time)
    _store('score_time', score_time)
    # Use one MaskedArray and mask all the places where the param is not
    # applicable for that candidate. Use defaultdict as each candidate may
    # not contain all the params
    param_results = defaultdict(partial(MaskedArray,
                                        np.empty(n_candidates,),
                                        mask=True,
                                        dtype=object))
    for cand_i, params in enumerate(candidate_params):
        for name, value in params.items():
            # An all masked empty array gets created for the key
            # `"param_%s" % name` at the first occurence of `name`.
            # Setting the value at an index also unmasks that index
            param_results["param_%s" % name][cand_i] = value

    results.update(param_results)
    # Store a list of param dicts at the key 'params'
    results['params'] = candidate_params

    # NOTE test_sample counts (weights) remain the same for all candidates
    test_sample_counts = np.array(test_sample_counts[:n_splits],
                                  dtype=np.int)
    for scorer_name in scorers.keys():
        # Computed the (weighted) mean and std for test scores alone
        _store('test_%s' % scorer_name, test_scores[scorer_name],
               splits=True, rank=True,
               weights=test_sample_counts if self.iid else None)
        if self.return_train_score:
            prev_keys = set(results.keys())
            _store('train_%s' % scorer_name, train_scores[scorer_name],
                   splits=True)

            if self.return_train_score == 'warn':
                for key in set(results.keys()) - prev_keys:
                    message = (
                        'You are accessing a training score ({!r}), '
                        'which will not be available by default '
                        'any more in 0.21. If you need training scores, '
                        'please set return_train_score=True').format(key)
                    # warn on key access
                    results.add_warning(key, message, FutureWarning)

    # For multi-metric evaluation, store the best_index_, best_params_ and
    # best_score_ iff refit is one of the scorer names
    # In single metric evaluation, refit_metric is "score"
    if self.refit or not self.multimetric_:
        self.best_index_ = results["rank_test_%s" % refit_metric].argmin()
        self.best_params_ = candidate_params[self.best_index_]
        self.best_score_ = results["mean_test_%s" % refit_metric][
            self.best_index_]

    if self.refit:
        self.best_estimator_ = clone(base_estimator).set_params(
            **self.best_params_)
        if y is not None:
            self.best_estimator_.fit(X, y, **fit_params)
        else:
            self.best_estimator_.fit(X, **fit_params)

    # Store the only scorer not as a dict for single metric evaluation
    self.scorer_ = scorers if self.multimetric_ else scorers['score']

    self.cv_results_ = results
    self.n_splits_ = n_splits

    return self
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    
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
        params = {}
        for key, value in search_space.items():
            params['clf__' + key] = value
        
        if args.condition == "fixed":
            # load default parameter setting
            with open('def_params.pickle', 'rb') as handle:
                def_params = pickle.load(handle)
            def_param = def_params[args.classifier][args.task_id][args.param]
            if args.param == 'max_features':
                # if max_features, either sqrt(n) ('auto) or ceiling(n**def_param)
                n_features = len(task.get_dataset().features)
                if args.deftype == 'sklearn':
                    def_param = 'auto'
                elif args.deftype == 'hyperimp':
                    def_param = int(np.ceil(n_features ** def_param))
            if args.param == 'gamma':
                # if gamma, either 1/n or just def_param
                n_features = len(task.get_dataset().features)
                if args.deftype == 'sklearn':
                    def_param = 'auto'
                elif args.deftype == 'hyperimp':
                    def_param = def_param
            if type(def_param) == np.bool_: #prevent JSON serializable error
                def_param = bool(def_param)
            if ((args.param == 'min_samples_leaf') or (args.param == 'min_samples_split')):
                def_param = int(def_param)
            # monkey patch fit function to add default parameter
            sklearn.model_selection.RandomizedSearchCV.fit = fit

        indices = task.get_dataset().get_features_by_type('nominal', [task.target_name])
        
        # set random generator seed to task_id
        random.seed(args.task_id)
        # generate the random seed that will be used in the random search
        rs_seed = [random.randint(0,1000000) for i in range(0,args.seed)][args.seed - 1]
        
        rscv = hyperimp.experiment.generate.build_rscv(args.classifier, indices, args.n_iter, rs_seed, args.cv, params)
        
        # run experiment
        run_experiment(rscv, task, args)
        
    except Exception as e:
        print("%s Error in run: %s" % (hyperimp.utils.get_time(), e))
        #traceback.print_exc()