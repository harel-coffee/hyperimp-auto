#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:01:59 2018

@author: hildeweerts

"""

"""
Set of function that can be used to evaluate fixed v.s. non-fixed experiments.
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import wilcoxon

def generate_data(df, parameter, lb, ub):
    # find fixed parameter data for 
    df_fix = df[df['fixed_param'] == parameter]
    df_fix = df_fix.astype({'fixed_value' : 'float'}).reset_index(drop = True)
    df_fix = df_fix[
        (df_fix['fixed_value'] >= lb) & 
        (df_fix['fixed_value'] <= ub)]

    datasets = df_fix['dataset'].unique()

    # find overall best accuracy scores per dataset per fold
    df_overall = pd.DataFrame()
    for dataset, data in df.groupby('dataset'):
        if dataset in datasets:
            top10 = pd.DataFrame()
            for fold, fold_data in data.groupby('fold'):
                top_fold = fold_data.sort_values('accuracy', ascending = False)[0:1]
                top10 = top10.append(top_fold)
            #top10 = data.sort_values('accuracy', ascending = False)[0:10]
            top10['dataset'] = dataset
            df_overall = df_overall.append(top10)
    
    # Create dataset with fixed and overall results
    df_overall['type'] = 'overall'
    df_fix['type'] = 'fixed'

    data = df_overall[['dataset', 'accuracy', 'type']].append(
        df_fix[['dataset', 'accuracy', 'type']]).reset_index(drop = True)
    return data

def omega_squared(aov):
    mse = aov['sum_sq'][-1]/aov['df'][-1]
    aov['omega_sq'] = 'NaN'
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*mse))/(sum(aov['sum_sq'])+mse)
    return aov

def aov(data):
    formula = 'accuracy ~ C(type) + C(dataset) + C(type):C(dataset)'
    model = ols(formula, data).fit()
    aov_table = anova_lm(model, typ=2)
    aov_table = omega_squared(aov_table)
    return model, aov_table

def boxplot(cols, data):
    nr_plots = len(data)/10
    rows = math.ceil(nr_plots/cols)
    fig = plt.figure(figsize = (4*cols,3*rows))
    index = 1
    for key_dataset, df in data.groupby('dataset'):
        ax = fig.add_subplot(rows, cols, index)
        ax.set_title('Dataset: %s' % key_dataset)
        series = []
        labels = []
        for key_type, df2 in df.groupby('type'):
            series.append(df2['accuracy'])
            labels.append(key_type)
        ax.boxplot(series, labels = labels, sym = 'k.')
        plt.tight_layout()
        index += 1
    plt.show()
    return

def wilcox(data):
    means = []
    for fix_type, fix_data in data.groupby('type'):
        means.append(fix_data.groupby('dataset').mean()['accuracy'])
    # perform wilcoxon signed rank test
    T, p = wilcoxon(means[1], means[0])
    return T, p