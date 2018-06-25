# hyperimp

Benchmark study on the importance of hyperparameter tuning: which parameters are important to tune and which can be set to a default value?

## Directories
A short explanation of the directory structure of this repository.

* **experiment_1**: In experiment 1, we generate random hyperparameter configurations, train simple pipelines, and upload the results to OpenML.
This directory contains all files necessary to run a docker container to run an instantiation the experiment.
* **experiment_2**: In experiment 2, we compare the performance of a model on a task when tuning all hyperparameters ('non-fixed') v.s. tuning all hyperparameters but leaving one hyperparameter fixed to the default value determined in experiment 1 ('fixed). This directory contains all files necessary to run a docker container to run an instantiation the experiment. One instantiation consists of a nested 10 x 5 cross validation. A random search is used to tune the hyperparameters in the inner loop.
* **batch-shipyard_1**: Directions and files necessary to run experiment 1 as a Azure batch job.
* **batch-shipyard_2**: Directions and files necessary to run experiment 2 as a Azure batch job.
* **hyperimp**: Python module used to evaluate the experiments.
* **01 data**: Data obtained from OpenML, partly preprocessed. 
* **02 figures**: All figures resulting from the analysis.

## Files
* `analysis experiment 1.ipynb`
Analysis of the results of experiment 1. Performance data is analyzed and default values are computed.

* `analysis experiment 2.ipynb`
Analysis of the results of experiment 2. Includes average ranks over number of iterations, tunability, and non-inferiority tests.

* [reflection.md](reflection.md)
Some general tips, tricks, and other reflections related to performing experiments on Azure and OpenML using dockerized experiment scripts.

## 
We thank Microsoft Azure for providing the computational resources for this study.
