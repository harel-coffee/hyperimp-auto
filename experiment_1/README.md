# Running experiment 1
This docker image can be used to run random configurations of an algorithm (including a simple preprocessing pipeline) and publish the results to OpenML. At this point only "svm" and "random_forest" are supported. The search space of the algorithms is defined in the file [search_space.py](hyperimp/study/search_space.py). The training timeout time of a single experiment is 40 minutes.

## Retrieve docker image
You can build the docker image from this repository in the following way.
1. Open terminal and go to this directory
2. Run `docker build -t $IMAGENAME .` where `$IMAGENAME` will be the name of the image. If docker complains that your forgot an argument you forgot to type the dot.

Alternatively, you can pull the docker image from docker hub directly by running `docker pull hilde/experiment_1`.

## Run an experiment
An example on how to run an experiment for a specific set of tasks is shown below.
```
docker run -a STDOUT \
--name $CONTAINERNAME hilde/experiment_1 \
--task_ids 3 6 11 \
--classifier svm \
--openml_apikey $APIKEY \
--num 1000
```
Where you replace `$CONTAINERNAME` with the name you want to give to the docker container, and `$APIKEY` with your OpenML apikey. Logging information will be printed realtime in the terminal, but can also be retrieved using `docker logs $CONTAINERNAME`.

It is also possible to immediately run all tasks from an OpenML study. An example on how to run an experiment for random forest for study 98 is shown below.
```
docker run -a STDOUT \
    --name $CONTAINERNAME hilde/experiment_1 \
    --study_id 98 \
    --classifier random_forest \
    --openml_apikey $APIKEY \
    --num 1000
```
Note that the `task_ids` argument takes priority over the `study_id` argument (i.e. if both are provided, the tasks listed in `task_ids` will be used rather than the tasks retrieved from the OpenML study).

## Retrieve log data
If, for some reason, runs could not be uploaded to OpenML, the predictions.csv, run.xml, and parameters.pickle files can be retrieved by running `docker cp $CONTAINERNAME:/root/results ./experiments` (i.e. they will be put in the folder /experiments of your local machine).

## Run experiment on Azure
To run the experiment on Azure, you can use docker-machine in the cloud shell of the portal.

1. Save your account id by running `sub=$(az account show --query "id" -o tsv)`.
2. To e.g. use a machine of the type F16s v2, located in the west of the united state, you run the following code:
    ```
    docker-machine create -d azure \
    --azure-subscription-id $sub \
    --azure-ssh-user azureuser \
    --azure-open-port 80 \
    --azure-location westus2 \
    --azure-size "Standard_F16s_v2" \
    myvm
    ```
    Where you replace `myvm` with whatever name you find appropriate for your machine.
3. Check if the machine is running properly, by running `docker-machine ls`. If it is not running, start it by running `docker-machine start myvm`.
4. Perform some magic to make sure the deamon is alive `eval $(docker-machine env myvm --shell bash)`.
5. Actually run your container by running the same command we've seen before.

