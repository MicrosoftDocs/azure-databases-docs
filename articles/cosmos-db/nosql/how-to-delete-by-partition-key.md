---
title:  Delete items by partition key value using the Azure Cosmos DB SDK (preview)
description: Learn how to delete items by partition key value using the Azure Cosmos DB SDKs
author: richagaur
ms.author: richagaur
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 05/23/2023
---

# Delete items by partition key value - API for NoSQL (preview)
[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

This article explains how to use the Azure Cosmos DB SDKs to delete all items by logical partition key value. 

> [!IMPORTANT]
> Delete items by partition key value is in public preview.
> This feature is provided without a service level agreement.
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Feature overview
 
The delete by partition key feature is an asynchronous, background operation that allows you to delete all documents with the same logical partition key value, using the Cosmos SDK.

Because the number of documents to be deleted may be large, the operation runs in the background. Though the physical deletion operation runs in the background, the effects are available immediately, as the documents to be deleted won't appear in the results of queries or read operations. 

The delete by partition key operation aims to consume at most 10% of the total available RU/s on the container each second on **best effort** basis. This helps in limiting the resources used by this background task.

## Getting started

Update your Azure Cosmos DB account to enable "Delete by partition key" feature using Azure CLI.

- Step 1: Set shell variables 
    ```azurecli-interactive
        $resourceGroupName = <azure_resource_group>
        $accountName = <azure_cosmos_db_account_name>
        $DeleteByPk = "DeleteAllItemsByPartitionKey"
    ```
- Step 2: List down existing capabilities of your account.
    ```azurecli-interactive
       $cosmosdb = az cosmosdb show \
        --resource-group $resourceGroupName \
        --name $accountName
       $capabilities = ($cosmosdb | ConvertFrom-Json).capabilities 
    ```
- Step 3: Add "Delete items by partition key" capability in the list of capabilities if it doesn't exist already. 
    > [!NOTE]
    > The list of capabilities must always specify all capabilities that you want to enable, inclusively. This includes capabilities that are already enabled for the account that you want to keep. 

    ```azurecli-interactive
       $capabilities = $DeleteByPk
    ```

- Step 4: Update Cosmos DB account to enable "Delete items by partition key" feature
    ```azurecli-interactive
        az cosmosdb update --capabilities $capabilities \
         -n $accountName -g $resourceGroupName
    ```

#### [.NET](#tab/dotnet-example)

## Sample code
Use [version 3.25.0-preview](https://www.nuget.org/packages/Microsoft.Azure.Cosmos) (or a higher preview version) of the Azure Cosmos DB .NET SDK to delete items by partition key. 

```csharp
// Suppose our container is partitioned by tenantId, and we want to delete all the data for a particular tenant Contoso

// Get reference to the container
var container = cosmosClient.GetContainer("DatabaseName", "ContainerName");

// Delete by logical partition key
ResponseMessage deleteResponse = await container.DeleteAllItemsByPartitionKeyStreamAsync(new PartitionKey("Contoso"));

 if (deleteResponse.IsSuccessStatusCode) {
    Console.WriteLine($"Delete all documents with partition key operation has successfully started");
}
```
#### [Java](#tab/java-example)

Use [version 4.19.0](https://mvnrepository.com/artifact/com.azure/azure-cosmos) (or a higher version) of the Azure Cosmos DB Java SDK to delete items by partition key. The delete by partition key API will be marked as beta.


```java
// Suppose our container is partitioned by tenantId, and we want to delete all the data for a particular tenant Contoso

// Delete by logical partition key
CosmosItemResponse<?> deleteResponse = container.deleteAllItemsByPartitionKey(
            new PartitionKey("Contoso"), new CosmosItemRequestOptions()).block();
```

#### [Python](#tab/python-example)

Use [beta-version ( >= 4.4.0b1)](https://pypi.org/project/azure-cosmos/4.4.0b1/) of the Azure Cosmos DB Python SDK to delete items by partition key. The delete by partition key API will be marked as beta.


```python
# Suppose our container is partitioned by tenantId, and we want to delete all the data for a particular tenant Contoso

# Delete by logical partition key
container.delete_all_items_by_partition_key("Contoso")

```

--- 

### Frequently asked questions (FAQ)
#### Are the results of the delete by partition key operation reflected immediately?
Yes, once the delete by partition key operation starts, the documents to be deleted won't appear in the results of queries or read operations. This also means that you can write new a new document with the same ID and partition key as a document to be deleted without resulting in a conflict.

See [Known issues](#known-issues) for exceptions. 

#### What happens if I issue a delete by partition key operation, and then immediately write a new document with the same partition key?
When the delete by partition key operation is issued, only the documents that exist in the container then with the partition key value will be deleted. Any new documents that come in won't be in scope for the deletion. 

### How is the delete by partition key operation prioritized among other operations against the container?
By default, the delete by partition key value operation can consume up to a reserved fraction - 0.1, or 10% - of the overall RU/s on the resource. Any Request Units (RUs) in this bucket that are unused will be available for other nonbackground operations, such as reads, writes, and queries. 

For example, suppose you've provisioned 1000 RU/s on a container. There's an ongoing delete by partition key operation that consumes 100 RUs each second for 5 seconds. During each of these 5 seconds, there are 900 RUs available for nonbackground database operations. Once the delete operation is complete, all 1000 RU/s are now available again. 

### Known issues
In some scenarios, a delete by partition key operation may not immediately guarantee its effects, and partial visibility may occur during the operation. 

- Aggregate queries that use the index - for example, COUNT queries - that are issued during an ongoing delete by partition key operation may contain the results of the documents to be deleted. This may occur until the delete operation is fully complete.
- Queries issued against the [analytical store](../analytical-store-introduction.md) during an ongoing delete by partition key operation may contain the results of the documents to be deleted. This may occur until the delete operation is fully complete.
- [Continuous backup (point in time restore)](../continuous-backup-restore-introduction.md) - a restore that is triggered during an ongoing delete by partition key operation may contain the results of the documents to be deleted in the restored collection. It isn't recommended to use this preview feature if you have a scenario that requires continuous backup.

### Limitations
- [Hierarchical partition keys](../hierarchical-partition-keys.md) deletion isn't supported. This feature permits the deletion of items solely based on the last level of partition keys. For example, consider a scenario where a partition key consists of three hierarchical levels: country/region, state, and city. In this context, the delete by partition keys functionality can be employed effectively by specifying the complete partition key, encompassing all levels, namely country/region, state, and city. Attempting to delete using intermediate partition keys, such as country/region or state, or solely country/region, will result in an error.

## How to give feedback or report an issue/bug
* Email cosmosPkDeleteFeedbk@microsoft.com with questions or feedback.

### SDK requirements

Find the latest version of the SDK that supports this feature.

| SDK | Supported versions | Package manager link |
| --- | --- | --- |
| **.NET SDK v3** | *>= 3.25.0-preview (must be preview version)* | <https://www.nuget.org/packages/Microsoft.Azure.Cosmos/> |
| **Java SDK v4** | *>= 4.19.0 (API is marked as beta)* | <https://mvnrepository.com/artifact/com.azure/azure-cosmos> |
| **Python SDK v4** | *>= 4..4.0b1 (must be beta version)* | <https://pypi.org/project/azure-cosmos/4.4.0b1/> |

Support for other SDKs is planned for the future.

## Next steps

See the following articles to learn about more SDK operations in Azure Cosmos DB.
- [Query an Azure Cosmos DB container](how-to-query-container.md)
- [Transactional batch operations in Azure Cosmos DB using the .NET SDK](transactional-batch.md)
