---
title: Container Copy Jobs
titleSuffix: Azure Cosmos DB
description: Learn how to copy data from one container to another in Azure Cosmos DB (preview).
author: richagaur
ms.author: richagaur
ms.service: azure-cosmos-db
ms.topic: how-to
ms.date: 06/23/2025
ms.custom: references_regions, build-2023, ignite-2023, ignite-2024
zone_pivot_groups: azure-cosmos-db-apis-nosql-mongodb-cassandra
---

# Copy jobs in Azure Cosmos DB (preview)

You can perform data copy in Azure Cosmos DB by using container copy jobs.

You might need to copy data from your Azure Cosmos DB account if you want to achieve any of these scenarios:

* Copy all items from one container to another.
* Change the [granularity at which throughput is provisioned, from database to container](set-throughput.md) and vice versa.
* Change the [partition key](partitioning-overview.md#choose-a-partition-key) of a container.
* Update the [unique keys](unique-keys.md) for a container.
* Rename a container or database.
* Change capacity mode of an account from serverless to provisioned or vice-versa.
* Adopt new features that are supported only for new containers, for example, [hierarchical partition keys](hierarchical-partition-keys.md).

Copy jobs can be [created and managed by using Azure CLI commands](how-to-container-copy.md).

::: zone pivot="api-nosql"

## Getting started

### [Online copy](#tab/online-copy)

#### Prerequisites

1. Enable [continuous backup](continuous-backup-restore-introduction.md) on source Azure Cosmos DB account. 
1. Enable [All version and delete change feed mode (preview)](change-feed-modes.md?tabs=all-versions-and-deletes#get-started) preview feature on the source account.

#### Enable Online copy

To enable online copy on your source account, execute following steps using [Azure CLI](/cli/azure/install-azure-cli).

```azurecli
# Set shell variables.
 $resourceGroupName = <azure_resource_group>
 $accountName = <azure_cosmos_db_account_name>
 $EnableOnlineContainerCopy = "EnableOnlineContainerCopy"

# List down existing capabilities of your account.
 $cosmosdb = az cosmosdb show \
    --resource-group $resourceGroupName \
    --name $accountName

$capabilities = (($cosmosdb | ConvertFrom-Json).capabilities)

# Append EnableOnlineContainerCopy capability in the list of capabilities.
 $capabilitiesToAdd = @()
 foreach ($item in $capabilities) {
    $capabilitiesToAdd += $item.name
 }
 $capabilitiesToAdd += $EnableOnlineContainerCopy

 # Update Cosmos DB account
 az cosmosdb update --capabilities $capabilitiesToAdd \
    -n $accountName -g $resourceGroupName
```

> [!IMPORTANT]
> All write operations on the source account are charged double RUs in order to preserve both the previous and current versions of changes to items in the container. This RU charge increase is subject to change in the future.

## Copy a container's data

1. Create the target Azure Cosmos DB container by using the settings that you want to use (partition key, throughput granularity, request units, unique key, and so on).
1. [Create the container copy job](how-to-container-copy.md).
1. [Monitor the progress of the copy job](how-to-container-copy.md#monitor-the-progress-of-a-copy-job).
1. After all documents are copied, stop the updates on source container, and then call the completion API to mark job as completed.
1. Resume the operations by appropriately pointing the application or client to the source or target container as intended.

## How does container copy work?

1. The platform allocates server-side compute instances for the destination Azure Cosmos DB account to run the container copy jobs.
1. A single job is executed across all instances at any time.
1. The online copy jobs utilize [all version and delete change feed mode](change-feed-modes.md?tabs=latest-version#all-versions-and-deletes-change-feed-mode-preview) to copy the data and replicate incremental changes from the source container to the destination container. 
1. Once the job is completed, the platform deallocates these instances after 15 minutes of inactivity.

### [Offline copy](#tab/offline-copy)

Start using offline copy by following [how to create, monitor, and manage copy jobs.](how-to-container-copy.md)

## Copy a container's data 

1. Create the target Azure Cosmos DB container by using the settings that you want to use (partition key, throughput granularity, request units, unique key, and so on).
1. Stop the operations on the source container by pausing the application instances or any clients that connect to it.
1. [Create the container copy job](how-to-container-copy.md).
1. [Monitor the progress of the container copy job](how-to-container-copy.md#monitor-the-progress-of-a-copy-job) and wait until it completes.
1. Resume the operations by appropriately pointing the application or client to the source or target container as intended.

> [!NOTE]
>  We strongly recommend that you stop performing any operations on the source container before you begin the offline container copy job. Item deletions and updates that are done on the source container after you start the copy job might not be captured. If you continue to perform operations on the source container while the container job is in progress, you might have duplicate or missing data on the target container.

## How does container copy work?

1. The platform allocates server-side compute instances for the destination Azure Cosmos DB account.
1. These instances are allocated when one or more container copy jobs are created within the account.
1. The container copy jobs run on these instances.
1. A single job is executed across all instances at any time.
1. The instances are shared by all the container copy jobs that are running within the same account.
1. The offline copy jobs utilize [Latest version change feed mode](change-feed-modes.md?tabs=latest-version#latest-version-change-feed-mode) to copy the data and replicate incremental changes from the source container to the destination container.
1. The platform might deallocate the instances if they're idle for longer than 15 minutes.

::: zone-end

::: zone pivot="api-mongodb"

You can perform offline collection copy jobs to copy data within the same Azure Cosmos DB for Mongo DB account.

## Copy a collection's data 

1. Create the target Azure Cosmos DB collection by using the settings that you want to use (partition key, throughput granularity, request units, unique key, and so on).
1. Stop the operations on the source collection by pausing the application instances or any clients that connect to it.
1. [Create the copy job](how-to-container-copy.md).
1. [Monitor the progress of the copy job](how-to-container-copy.md#monitor-the-progress-of-a-copy-job) and wait until it completes.
1. Resume the operations by appropriately pointing the application or client to the source or target collection as intended.

> [!NOTE]
>  We strongly recommend that you stop performing any operations on the source collection before you begin the offline collection copy job. Item deletions and updates that are done on the source collection after you start the copy job might not be captured. If you continue to perform operations on the source collection while the copy job is in progress, you might have duplicate or missing data on the target collection.

## How does collection copy work?

1. The platform allocates server-side compute instances for the destination Azure Cosmos DB account.
1. These instances are allocated when one or more collection copy jobs are created within the account.
1. The copy jobs run on these instances.
1. A single job is executed across all instances at any time.
1. The instances are shared by all the copy jobs that are running within the same account.
1. The offline copy jobs utilize [Change streams](mongodb/change-streams.md?tabs=javascript) to copy the data and replicate incremental changes from the source collection to the destination collection.
1. The platform might deallocate the instances if they're idle for longer than 15 minutes.

::: zone-end

::: zone pivot="api-apache-cassandra"

You can perform offline table copy to copy data of one table to another table within the same Azure Cosmos DB for Apache Cassandra account.

## Copy a table's data 

1. Create the target Azure Cosmos DB table by using the settings that you want to use (partition key, throughput granularity, request units, and so on).
1. Stop the operations on the source table by pausing the application instances or any clients that connect to it.
1. [Create the copy job](how-to-container-copy.md).
1. [Monitor the progress of the copy job](how-to-container-copy.md#monitor-the-progress-of-a-copy-job) and wait until it completes.
1. Resume the operations by appropriately pointing the application or client to the source or target table as intended.

> [!NOTE]
>  We strongly recommend that you stop performing any operations on the source table before you begin the offline table copy job. Item deletions and updates that are done on the source table after you start the copy job might not be captured. If you continue to perform operations on the source table while the copy job is in progress, you might have duplicate or missing data on the target table.

## How does table copy work?

1. The platform allocates server-side compute instances for the destination Azure Cosmos DB account.
1. These instances are allocated when one or more copy jobs are created within the account.
1. The copy jobs run on these instances.
1. A single job is executed across all instances at any time.
1. The instances are shared by all the copy jobs that are running within the same account.
1. The offline copy jobs utilize [Change feed](cassandra/change-feed.md) to copy the data and replicate incremental changes from the source table to the destination table.
1. The platform might deallocate the instances if they're idle for longer than 15 minutes.

::: zone-end

## Factors that affect the rate of a copy job

The rate of container copy job progress is determined by these factors:

* The source container or database throughput setting.

* The target container or database throughput setting.

   > [!TIP]
   > Set the target container throughput to at least two times the source container's throughput.

* Server-side compute instances that are allocated to the Azure Cosmos DB account for performing the data transfer.

   > [!IMPORTANT]
   > The default SKU offers two 4-vCPU 16-GB server-side instances per account.

## Limitations

### Preview eligibility criteria

Container copy jobs don't work with accounts that have the following capabilities enabled. Disable these features before you run container copy jobs:

* [Merge partition](merge.md)

### Account configurations

The Time to Live (TTL) setting isn't adjusted in the destination container. As a result, if a document hasn't expired in the source container, it starts its countdown anew in the destination container.

## Frequently asked questions

### Is there a service-level agreement for container copy jobs?

Container copy jobs are currently supported on a best-effort basis. We don't provide any service-level agreement (SLA) guarantees for the time it takes for the jobs to finish.

### Can I create multiple container copy jobs within an account?

Yes, you can create multiple jobs within the same account. The jobs run consecutively. You can [list all the jobs](how-to-container-copy.md#list-all-the-copy-jobs-created-in-an-account) that are created within an account, and monitor their progress.

### Can I copy an entire database within the Azure Cosmos DB account?

You must create a job for each container in the database.

### I have a Cosmos DB account with multiple regions. In which region will the container copy job run?

The container copy job runs in the write region. In an account that's configured with multi-region writes, the job runs in one of the regions in the list of write regions.

### What happens to the container copy jobs when the account's write region changes?

The account's write region might change in the rare scenario of a region outage or due to manual failover. In this scenario, incomplete container copy jobs that were created within the account fail. You would need to re-create these failed jobs. Re-created jobs then run in the new (current) write region.

## Supported regions

Currently, container copy is supported in the following regions:

| Americas | Europe and Africa | Asia Pacific |
| ------------ | -------- | ----------- |
| Brazil South | France Central | Australia Central |
| Canada Central | France South | Australia Central 2 |
| Canada East | Germany North | Australia East |
| Central US | Germany West Central | Central India |
| Central US EUAP | North Europe | Japan East |
| East US | Norway East | Korea Central |
| East US 2 | Norway West | Southeast Asia |
| East US 2 EUAP | Switzerland North | UAE Central |
| North Central US | Switzerland West | West India |
| South Central US | UK South | East Asia |
| West Central US | UK West  | Malaysia South |
| West US | West Europe | Japan West |
| West US 2 | Israel Central | Australia Southeast |
| Not supported | South Africa North | Not supported | 


## Known and common issues

* While using the online container copy feature, if the `id` field is modified in the source container, the destination container stores two separate documents, each corresponding to the distinct `id` values. 

* When changing partition keys during data copying to the destination container, ensure that the new partition key and `id` combinations are unique across the container. 

    For example, consider the following scenario:

    **Original Partition Key:** `/department`  
    **Source Documents:**

    ```json
    {
        "id": "101",
        "employeeName": "John Doe",
        "department": "HR"
    },
    {
        "id": "101",
        "employeeName": "John Doe",
        "department": "Finance"
    }
    ```

    **New Partition Key:** `/employeeName`  
    **Resulting Documents in the Destination Container:**

    ```json
    {
        "id": "101",
        "employeeName": "John Doe",
        "department": "HR"
    },
    {
        "id": "101",
        "employeeName": "John Doe",
        "department": "Finance"
    }
    ```

    In this case, both documents now share the same partition key (`/employeeName`) and `id` combination (`"employeeName": "John Doe", "id": "101"`), which causes a conflict. This conflict results in an insertion error. To avoid such issues, ensure that the new partition key and `id` combinations are unique across all documents in the destination container.

* Error - Partition key reached maximum size of 20 GB

    When modifying partition keys during data copy to the destination container, ensure that the new partition key remains within the logical partition key size limit of 20 GB. If this limit is exceeded, the job fails with the following error:

    ```output
    "code": "403",
    "message": "Response status code does not indicate success: Forbidden (403); Substatus: 1014; ActivityId: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx; Reason: (Message: {"Errors":["Partition key reached maximum size of 20 GB. Learn more: https://aka.ms/CosmosDB/sql/errors/full-pk"]"
    ```

* Error - Owner resource doesn't exist

    If the job creation fails and displays the error "Owner resource doesn't exist" (error code 404), either the target container hasn't been created yet or the container name that's used to create the job doesn't match an actual container name.

    Make sure that the target container is created before you run the job and ensure that the container name in the job matches an actual container name.

    ```output
    "code": "404",
    "message": "Response status code does not indicate success: NotFound (404); Substatus: 1003; ActivityId: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx; Reason: (Message: {\"Errors\":[\"Owner resource does not exist\"]
    ```

* Error - Error while getting resources for job

    This error might occur due to internal server issues. To resolve this issue, contact Microsoft Support by opening a **New Support Request** in the Azure portal. For **Problem Type**, select **Data Migration**. For **Problem subtype**, select **Intra-account container copy**.

    ```output
    "code": "500"
    "message": "Error while getting resources for job, StatusCode: 500, SubStatusCode: 0, OperationId:  xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx, ActivityId: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ```

## Next step

* [Create and manage container copy jobs in Azure Cosmos DB](how-to-container-copy.md)
