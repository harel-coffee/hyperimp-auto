# Running experiment 1 using batch-shipyard

## Create Batch and storage account
First, we need to create an Azure Batch account and storage account. This can be done on portal.azure.com.
Note the account service URL and account key after creating the Batch account.
Note the storage account name nad account key after creating your Storage account.
Or not. It's your life. But you're going to need them in the next step.

## Upload configure files to Azure
1. Adapt the configure file templates in [config](config) to fit your needs.
    * `credentials.yaml`: this file configures the credentials of the batch account and storage account. You can find the keys and urls of the accounts you created in the previous step in the Azure portal. 
    *`jobs.yaml`: this file contains configurations of the jobs and tasks you want to run. The `command` line contains settings you would normally add to `docker run`.  Automatically retrieving all tasks from a specific study is not supported at this point. But you can use [gen_tasks.py](gen_tasks.py) and copy paste it from there.
    *`pool.yaml`: this file contains information about the pool of nodes you want to use for the experiment. You can set e.g. the number and type of virtual machines. 
    *`config.yaml`: you do not need to change anything in this file, unless you want to use e.g. a different docker image.
2. Open a Cloud Shell session on the Azure portal. Create a new directory to store the configure files: `mkdir config`
3. Upload the configure files using the upload button.
4. Move the configure files to the `config` directory: `mv *.yaml config/`

## Add pool and job
1. Open a Cloud shell session and run the folloiwng command:
    ```
    SHIPYARD_CONFIGDIR=config shipyard pool add
    ```
    this will create a new pool of nodes. This may take a while.
2. Add the jobs by running the following command:
    ```
    SHIPYARD_CONFIGDIR=config shipyard jobs add --tail stdout.txt --tail stderr.txt
    ```

## Check progress
If you're interested in a nice app to keep track of your tasks that does not have a horrible, irresponsive design (I'm talking to you, Azure portal) consider downloading BatchLabs (https://azure.github.io/BatchLabs/).

## Delete pool and job
Don't forget to delete your jobs and tasks when you're done. Otherwise Microsoft will charge you.
Delete jobs:
```
SHIPYARD_CONFIGDIR=config shipyard jobs del -y --wait
```
Delete pool:
```
SHIPYARD_CONFIGDIR=config shipyard pool del -y
```
You can also do this in BatchLabs (try not to accidentally remove your Batch account as well).
