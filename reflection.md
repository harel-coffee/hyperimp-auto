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
With Docker for Azure, you can launch a Docker swarm including workers, managers, load balancing, and all other sorts of fun things. However, it seems to be mostly meant for web applications rather than a fixed set of experiments. So for benchmarking experiments, this is probably not the best option.

Info: https://www.docker.com/docker-azure

#### 2. docker-machine
An easy way to run a docker container on Azure is by using docker-machine. You can immediately use `docker-machine create` commands in the Cloud Shell environment in the Azure portal. This will create a linux virtual machine with docker installed. Once you are connected to the VM you can use regular docker commands to run your containers. 

_Advantages_: very easy to setup, all VMs are available (e.g. 72-core beasts)
_Disdadvantages_: if you want to run many experiments, quite some manual work is involved

Info: https://docs.microsoft.com/en-us/azure/virtual-machines/linux/docker-machine

#### 3. batch-shipyard 
Batch shipyard is a docker-friendly module that uses batch services. The 

_Advantage_: Very nice maintainer that will answer your questions on Github (so no support request required!).
_Disadvantage_: 

Info: http://batch-shipyard.readthedocs.io/

## OpenML

### Add retry to any API call; 
preferably with random number of seconds (e.g. between 5 and 60 seconds). Otherwise you might feel like you’re performing a DoS attack on the OpenML server (which feels pretty badass until you realise you’re only hurting yourself).

### The evaluation engine can be slow
At this point, a single evaluation can take up to 20 seconds.
