---
title: Create and Manage Intra-account Container Copy Jobs
description: Learn how to create, monitor, and manage container copy jobs within an Azure Cosmos DB account using CLI commands.
author: richagaur
ms.service: azure-cosmos-db
ms.custom: devx-track-azurecli, build-2023, ignite-2023, ignite-2024
ms.topic: how-to
ms.date: 06/26/2025
ms.author: richagaur
zone_pivot_groups: azure-cosmos-db-apis-nosql-mongodb-cassandra
appliesto:
  - ✅ NoSQL
---

# Create and manage container copy jobs in Azure Cosmos DB (Preview)

[Copy jobs](container-copy.md) help create copies of containers in Azure Cosmos DB accounts.

This article describes how to create, monitor, and manage copy jobs using Azure CLI commands.

## Prerequisites

* You can use the portal [Cloud Shell](/azure/cloud-shell/quickstart?tabs=powershell) to run container copy commands. Alternately, you can run the commands locally. Make sure you have [Azure CLI](/cli/azure/install-azure-cli) installed on your machine.
* Currently, container copy is only supported in [these regions](container-copy.md#supported-regions). Make sure your account's write region belongs to this list.
* Install the Azure Cosmos DB preview extension, which contains the container copy commands.
    ```azurecli-interactive
    az extension add --name cosmosdb-preview
    ```

::: zone pivot="api-nosql"

### [Online container copy](#tab/online-copy)

### Set shell variables

First, set all of the variables that each individual script uses.

```azurecli-interactive
$sourceSubId = "<source-subscription-id>" 
$destinationSubId = "<destination-subscription-id>" 
$sourceAccountRG = "<source-resource-group-name>"
$destinationAccountRG = "<destination-resource-group-name>"
$sourceAccount = "<cosmos-source-account-name>"
$destinationAccount = "<cosmos-destination-account-name>"
$jobName = ""
$sourceDatabase = ""
$sourceContainer = ""
$destinationDatabase = ""
$destinationContainer = ""
```

### Assign read permission

>[!Note]
> This step isn't required if you're copying data within the same Azure Cosmos DB account.

While copying data from one account's container to another account's container, you need to give read access for source container to the destination account's identity. Follow these steps to assign the required read permission to the destination account.

**Using system-managed identity**

1. Set destination subscription context:
    ```azurecli-interactive
    az account set --subscription $destinationSubId
    ```
1. Add system identity on destination account:
    ```azurecli-interactive
    $identityOutput = az cosmosdb identity assign -n $destinationAccount -g $destinationAccountRG
    $principalId = ($identityOutput | ConvertFrom-Json).principalId
    ```
1. Set default identity on destination account:
    ```azurecli-interactive
    az cosmosdb update -n $destinationAccount -g $destinationAccountRG --default-identity="SystemAssignedIdentity"
    ```
1. Set source subscription context:
    ```azurecli-interactive
    az account set --subscription $sourceSubId
    ```
1. Add role assignment on source account:
    ```azurecli-interactive
    # Read-only access role
    $roleDefinitionId = "00000000-0000-0000-0000-000000000001" 
    az cosmosdb sql role assignment create --account-name $sourceAccount --resource-group $sourceAccountRG --role-definition-id $roleDefinitionId --scope "/" --principal-id $principalId
    ```
1. Reset destination subscription context:
    ```azurecli-interactive
    az account set --subscription $destinationSubId
    ```

**Using user-assigned managed identity**

1. Assign user-assigned managed identity variable:
    ```azurecli-interactive
    $userAssignedManagedIdentityResourceId = "<CompleteResourceIdOfUserAssignedManagedIdentity>"
    ```
1. Set destination subscription context:
    ```azurecli-interactive
    az account set --subscription $destinationSubId
    ```
1. Add user-assigned managed identity on destination account:
    ```azurecli-interactive
    $identityOutput = az cosmosdb identity assign -n $destinationAccount -g $destinationAccountRG --identities $userAssignedManagedIdentityResourceId
    $principalId = ($identityOutput | ConvertFrom-Json).userAssignedIdentities.$userAssignedManagedIdentityResourceId.principalId
    ```
1. Set default identity on destination account:
    ```azurecli-interactive
    az cosmosdb update -n $destinationAccount -g $destinationAccountRG --default-identity=UserAssignedIdentity=$userAssignedManagedIdentityResourceId
    ```
1. Set source subscription context:
    ```azurecli-interactive
    az account set --subscription $sourceSubId
    ```
1. Add role assignment on source account:
    ```azurecli-interactive
    $roleDefinitionId = "00000000-0000-0000-0000-000000000001"  # Read-only access role
    az cosmosdb sql role assignment create --account-name $sourceAccount --resource-group $sourceAccountRG --role-definition-id $roleDefinitionId --scope "/" --principal-id $principalId
    ```
1. Reset destination subscription context:
    ```azurecli-interactive
    az account set --subscription $destinationSubId
    ```

### Create copy job

```azurecli-interactive
az cosmosdb copy create `
    --resource-group $destinationAccountRG `
    --job-name $jobName `
    --dest-account $destinationAccount `
    --src-account $sourceAccount `
    --dest-nosql database=$destinationDatabase container=$destinationContainer `
    --src-nosql database=$sourceDatabase container=$sourceContainer
    --mode Online
```

### Monitor progress 

Monitor the progress using this command:

```azurecli-interactive
az cosmosdb copy show `
    --resource-group $destinationAccountRG `
    --account-name $destinationAccount `
    --job-name $jobName
```

- **Total count** represents the total number of changes (total document + any new changes) in the source container at any given time.
- **Processed count** represents the total number of events coming from source container’s change feed that were processed by the copy job.

### Complete copy job

1. When the processed count becomes greater than or equal to the total count, turn off any updates on the source container and wait for 5-10 minutes to flush any remaining changes. 
1. Run the completion API to finish the copy job and free compute resources, this also writes the remaining changes (if any) to the destination container.

```azurecli-interactive
    az cosmosdb copy complete `
        --resource-group $destinationAccountRG `
        --account-name $destinationAccount `
        --job-name $jobName
```

1. Update the client applications to start using the new (destination) container if needed.

### [Offline container copy](#tab/offline-copy)

### Set shell variables

First, set all of the variables that each individual script uses.

```azurecli-interactive
$sourceSubId = "<source-subscription-id>" 
$destinationSubId = "<destination-subscription-id>" 
$sourceAccountRG = "<source-resource-group-name>"
$destinationAccountRG = "<destination-resource-group-name>"
$sourceAccount = "<cosmos-source-account-name>"
$destinationAccount = "<cosmos-destination-account-name>"
$jobName = ""
$sourceDatabase = ""
$sourceContainer = ""
$destinationDatabase = ""
$destinationContainer = ""
```

### Assign read permission

>[!Note]
> This step isn't required if you're copying data within the same Azure Cosmos DB account.

While copying data from one account's container to another account's container, it's required to give read access of source container to destination account's identity to perform the copy operation. Follow these steps to assign requisite read permission to the destination account.

**Using system-managed identity**

1. Set destination subscription context:
    ```azurecli-interactive
    az account set --subscription $destinationSubId
    ```
1. Add system identity on destination account:
    ```azurecli-interactive
    $identityOutput = az cosmosdb identity assign -n $destinationAccount -g $destinationAccountRG
    $principalId = ($identityOutput | ConvertFrom-Json).principalId
    ```
1. Set default identity on destination account:
    ```azurecli-interactive
    az cosmosdb update -n $destinationAccount -g $destinationAccountRG --default-identity="SystemAssignedIdentity"
    ```
1. Set source subscription context:
    ```azurecli-interactive
    az account set --subscription $sourceSubId
    ```
1. Add role assignment on source account:
    ```azurecli-interactive
    # Read-only access role
    $roleDefinitionId = "00000000-0000-0000-0000-000000000001" 
    az cosmosdb sql role assignment create --account-name $sourceAccount --resource-group $sourceAccountRG --role-definition-id $roleDefinitionId --scope "/" --principal-id $principalId
    ```
1. Reset destination subscription context:
    ```azurecli-interactive
    az account set --subscription $destinationSubId
    ```

**Using user-assigned managed identity**

1. Assign user-assigned managed identity variable:
    ```azurecli-interactive
    $userAssignedManagedIdentityResourceId = "<CompleteResourceIdOfUserAssignedManagedIdentity>"
    ```
1. Set destination subscription context:
    ```azurecli-interactive
    az account set --subscription $destinationSubId
    ```
1. Add user-assigned managed identity on destination account:
    ```azurecli-interactive
    $identityOutput = az cosmosdb identity assign -n $destinationAccount -g $destinationAccountRG --identities $userAssignedManagedIdentityResourceId
    $principalId = ($identityOutput | ConvertFrom-Json).userAssignedIdentities.$userAssignedManagedIdentityResourceId.principalId
    ```
1. Set default identity on destination account:
    ```azurecli-interactive
    az cosmosdb update -n $destinationAccount -g $destinationAccountRG --default-identity=UserAssignedIdentity=$userAssignedManagedIdentityResourceId
    ```
1. Set source subscription context:
    ```azurecli-interactive
    az account set --subscription $sourceSubId
    ```
1. Add role assignment on source account:
    ```azurecli-interactive
    $roleDefinitionId = "00000000-0000-0000-0000-000000000001"  # Read-only access role
    az cosmosdb sql role assignment create --account-name $sourceAccount --resource-group $sourceAccountRG --role-definition-id $roleDefinitionId --scope "/" --principal-id $principalId
    ```
1. Reset destination subscription context:
    ```azurecli-interactive
    az account set --subscription $destinationSubId
    ```

### Create copy job

```azurecli-interactive
az cosmosdb copy create `
    --resource-group $destinationAccountRG `
    --job-name $jobName `
    --dest-account $destinationAccount `
    --src-account $sourceAccount `
    --dest-nosql database=$destinationDatabase container=$destinationContainer `
    --src-nosql database=$sourceDatabase container=$sourceContainer
```

> [!NOTE]
> `--job-name` should be unique for each job within an account.

::: zone-end

::: zone pivot="api-mongodb"

### Set shell variables

First, set all of the variables that each individual script uses.

```azurecli-interactive
$destinationRG = "<destination-resource-group-name>"
$sourceAccount = "<cosmos-source-account-name>"
$destinationAccount = "<cosmos-destination-account-name>"
$jobName = ""
$sourceDatabase = ""
$sourceCollection = ""
$destinationDatabase = ""
$destinationCollection = ""
```

### Create copy job

Create a job to copy a collection within an Azure Cosmos DB API for MongoDB account:

```azurecli-interactive
az cosmosdb copy create `
    --resource-group $destinationRG `
    --job-name $jobName `
    --dest-account $destinationAccount `
    --src-account $sourceAccount `
    --dest-mongo database=$destinationDatabase collection=$destinationCollection `
    --src-mongo database=$sourceDatabase collection=$sourceCollection 
```

> [!NOTE]
> `--job-name` should be unique for each job within an account.

::: zone-end

::: zone pivot="api-apache-cassandra"

### Set shell variables

First, set all of the variables that each individual script uses.

```azurecli-interactive
$destinationRG = "<destination-resource-group-name>"
$sourceAccount = "<cosmos-source-account-name>"
$destinationAccount = "<cosmos-destination-account-name>"
$jobName = ""
$sourceKeySpace = ""
$sourceTable = ""
$destinationKeySpace = ""
$destinationTable = ""
```

### Create copy job

Create job to copy a table within an Azure Cosmos DB for Apache Cassandra account:

```azurecli-interactive
az cosmosdb copy create `
    --resource-group $destinationRG `
    --job-name $jobName `
    --dest-account $destinationAccount `
    --src-account $sourceAccount `
    --dest-cassandra keyspace=$destinationKeySpace table=$destinationTable `
    --src-cassandra keyspace=$sourceKeySpace table=$sourceTable 
```

> [!NOTE]
> `--job-name` should be unique for each job within an account.

::: zone-end

## Managing copy jobs

### Monitor the progress of a copy job

View the progress and status of a copy job:

```azurecli-interactive
az cosmosdb copy show `
    --resource-group $destinationAccountRG `
    --account-name $destinationAccount `
    --job-name $jobName
```

### List all the copy jobs created in an account

To list all the copy jobs created in an account:

```azurecli-interactive
az cosmosdb copy list `
    --resource-group $destinationAccountRG `
    --account-name $destinationAccount
```

### Pause a copy job

In order to pause an ongoing copy job, you can use the command:

```azurecli-interactive
az cosmosdb copy pause `
    --resource-group $destinationAccountRG `
    --account-name $destinationAccount `
    --job-name $jobName
```

### Resume a copy job

In order to resume an ongoing copy job, you can use this command:

```azurecli-interactive
az cosmosdb copy resume `
    --resource-group $destinationAccountRG `
    --account-name $destinationAccount `
    --job-name $jobName
```

### Cancel a copy job

In order to cancel an ongoing copy job, you can use this command:

```azurecli-interactive
az cosmosdb copy cancel `
    --resource-group $destinationAccountRG `
    --account-name $destinationAccount `
    --job-name $jobName
```

## Get support for copy issues

For issues related to a copy job, raise a **New Support Request** from the Azure portal. Set the **Problem Type** as *Data Migration* and **Problem subtype** as *Container copy*.

## Next step

- For more information about container copy jobs, see [Copy jobs](container-copy.md).
