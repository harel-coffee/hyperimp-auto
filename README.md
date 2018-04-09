# hyperimp

Benchmark study on the importance of hyperparameter tuning: which parameters are important to tune and which can be set to a default value?

## Directories
A short explanation of the directory structure of this repository.

### experiment_1
In experiment 1, we generate random hyperparameter configurations, train simple pipelines, and upload the results to OpenML.
This directory contains all files necessary to run a docker container to run an instantiation the experiment.

### evaluate_1
Contains scripts to analyze the performance measurements generated in experiment 1. In particular, we determine default values.

### batch-shipyard_1
Directions and files necessary to run experiment 1 as a Azure batch job.
