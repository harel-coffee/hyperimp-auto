# Running docker

## Retrieve docker image
You can build the docker image from this repository in the following way.
1. Open terminal and go to this directory
2. Run `docker build -t $IMAGENAME .` where `$IMAGENAME` will be the name of the image.
Alternatively, you can pull the docker image from docker hub by running `docker pull hilde/experiment_1`.

## Run experiment
An example on how to run an experiment for random forest for study 98 is shown below.
```
docker run -a STDOUT \
    --name $CONTAINERNAME hilde/experiment_1 \
    --study_id 98 \
    --classifier random_forest \
    --openml_apikey $APIKEY \
    --num 1000 \
```
Where you replace `$CONTAINERNAME` with the name you want to give to the docker container, and `$APIKEY` with your OpenML apikey. The progress of the container will be printed realtime in the terminal, but can also be retrieved using `docker logs $CONTAINERNAME`.

## Retrieve log data
If, for some reason, runs could not be uploaded to OpenML, the predictions.csv, run.xml, and parameters.pickle files can be retrieved by running `docker cp $CONTAINERNAME:/root/results ./experiments`.

## Run experiment on Azure
To run the experiment on Azure, you can use docker-machine in the shell.

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

