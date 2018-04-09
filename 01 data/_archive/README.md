# Data 

## Hyperparameter Importance Across Datasets (openml-pimp)
Data related to the study _Hyperparameter Importance Across Datasets_

### Performance data 
Average accuracy scores of 10-fold cross validation accross 100 OpenML datasets
columns: hyperparameters, accuracy score (average over 10 folds), dataset id
* meta_adaboost.arff
* meta_random_forest.arff
* meta_svm.arff

### Verification experiment 
Accuracy scores per outer fold of 10 x 3 fold cross validation with one parameter fixed. 
columns: accuracy, fold, fixed_param, fixed_value, dataset
* verification_svm_rbf.csv
* verifcation_svm_sigmoid.csv
* verfication_rf.csv

### Uniform random search experiment
Accuracy scores per outer fold of 10 x 3 cross validation with no parameter fixed but with different seeds for the inner random search cross validation splits.
columns: accuracy, fold, dataset, seed
* rs_svm_rbf.csv
* rs_svm_sigmoid.csv
* rs_rf.csv

## Other data
### Characteristics of hyperparameters
columns: algorithm name, parameter name, integer range (T/F), logarithmic range (T/F)
* parameters.csv: information about hyperparameters

### Search space
dictionary with parameter ranges (scipy random variable and list objects) for each alg/param combination
* search_space_rv.pickle
