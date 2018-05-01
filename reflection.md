# Reflection
This document contains some general tips, tricks, and other reflections on life that might be useful for people that want to perform experiments similar to the ones executed for this project.

## Microsoft Azure

### Increase your core quota 
Before you do anything else, first request a core quota increase. There is a different quota for basically any service Microsoft Azure offers and the default quotas are rather limited. For example, you have core quota for specific regions, SKU types, batch jobs, batch cores, and so forth. Depending on the request it can take some time (e.g. a week) before your core quota is actually increased. Also note that some SKU types are not available for every service, e.g. at this point FSv2 SKUs are not yet available via Batch service.

You can request a core quota increase in the Azure portal at _Help + support_ > _New support request_. To speed up the process, include the following information in your request:

* SKU type: e.g. Dsv2
* Region: e.g. southeast asia
* Subscription ID: ...
* Current core quota: e.g. 1000
* Requested increase: e.g. 500
* New core quota: e.g. 1500

If you want to increase your batch core quota, also include the Batch account name and whether you want to increase the dedicated core quota or low priority core quota. Important: a batch quota is associated with a batch account; so try not to accidentally delete the account.

### There are roughly 1 million ways to run a docker container on Microsoft Azure
I will list three of them.

#### 1. Docker for Azure
With Docker for Azure, you can launch a Docker swarm including workers, managers, load balancing, etc. However, it seems to be mostly meant for web applications rather than a fixed set of experiments. So for benchmarking experiments, this is probably not the best option.

Info: https://www.docker.com/docker-azure

#### 2. docker-machine
An easy way to run a docker container on Azure is by using docker-machine. You can immediately use `docker-machine create` commands in the Cloud Shell environment in the Azure portal. This will create a linux virtual machine with docker installed. Once you are connected to the VM you can use regular docker commands to run your containers. 

_Advantages_: very easy to setup, all VMs are available (e.g. 72-core beasts)
_Disdadvantages_: if you want to run many experiments, quite some manual work is involved

Info: https://docs.microsoft.com/en-us/azure/virtual-machines/linux/docker-machine

#### 3. batch-shipyard 
Batch shipyard is a docker-friendly module that uses Azure batch services. You can use configure files to determine the size of the pool and the specific tasks that need to be performed (e.g. the commands of the docker container). Then, you can start your batch service with only a few lines of codes in Azure Cloud shell.

_Advantage_: easy way to run many tasks without much manual interventions, very nice maintainer that answers questions on Github very fast (so no support requests to Microsoft, hooray!)
_Disadvantage_: not all VM types are available

Info: http://batch-shipyard.readthedocs.io/

## OpenML

### Add retry to any API call
Preferably with random number of seconds (e.g. between 5 and 60 seconds). Otherwise you might feel like you’re performing a DoS attack on the OpenML server (which feels pretty badass until you realise you’re only hurting yourself).

### The evaluation engine can be slow
Every run you send to OpenML will be evaluated by the evaluation engine. However, when uploading many runs, the engine will often fall behind. A single evaluation takes about 10 to 20 seconds. You can ask an OpenML maintainer for extra evaluation engines dedicated to your experiments. You might consider storing the evaluations within your experiments instead.

### Retrieving traces can go wrong
When retrieving traces using e.g. `openml.runs.get_run_trace(run_id)`, you might get the following error:

'''
OpenMLServerException: No successful trace associated with this run.
'''

Often, however, there actually exists a successful trace on the server, but something went wrong during the evaluation. If that is the case, you can simply reset the run using the following API call: https://www.openml.org/api/v1/run/reset/run_id.
