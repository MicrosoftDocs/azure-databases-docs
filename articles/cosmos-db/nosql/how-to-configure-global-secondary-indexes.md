---
title: How to configure global secondary indexes (preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to configure global secondary indexes and use them to avoid expensive cross-partition queries.
author: jcocchi
ms.author: jucocchi
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 3/24/2025
---

# How to configure Azure Cosmos DB for NoSQL global secondary indexes (preview)

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

> [!IMPORTANT]
> Azure Cosmos DB for NoSQL global secondary indexes are currently in preview. You can enable this feature by using the Azure portal and the feature can't be disabled. This preview is provided without a service-level agreement. At this time, we don't recommend that you use global secondary indexes for production workloads. Certain features of this preview might not be supported or might have constrained capabilities. For more information, see the [supplemental terms of use for Microsoft Azure previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Global secondary indexes provide a powerful way to optimize query performance and simplify application logic by storing your data with a different partition key and/ or data model. This article describes how to create global secondary indexes and how to use them to handle cross-partition queries efficiently.

## Prerequisites

- An existing Azure Cosmos DB account.
  - If you have an Azure subscription, [create a new account](how-to-create-account.md?tabs=azure-portal).
  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.
  - Alternatively, you can [try Azure Cosmos DB free](../try-free.md) before you commit.

## Enable global secondary indexes

The global secondary index feature needs to be enabled for your Azure Cosmos DB account before provisioning a builder or creating index containers.

### [Azure portal](#tab/azure-portal)

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Go to your Azure Cosmos DB for NoSQL account.

1. In the resource menu, select **Settings**.

1. In the **Features** section under **Settings**, toggle the **Materialized Views for NoSQL API (preview)** option to **On**.

> [!NOTE]
> Materialized Views is the prior name for this feature. Enabling materialized views will also enable global secondary indexes. 

1. In the new dialog, select **Enable** to enable this feature for the account.

### [Azure CLI](#tab/azure-cli)

Use the Azure CLI to enable the global secondary index feature either by using a native command or a REST API operation on your Azure Cosmos DB for NoSQL account.

1. Sign in to the Azure CLI.

    ```azurecli
    az login
    ```

   > [!NOTE]
   > This requires the Azure CLI, see [how to install the Azure CLI](/cli/azure/install-azure-cli).

1. Define the variables for the resource group and account name of your existing Azure Cosmos DB for NoSQL account.

    ```azurecli
    # Variable for resource group name
    $resourceGroupName="<resource-group-name>"
    
    # Variable for account name
    $accountName="<account-name>"
    
    # Variable for Azure subscription
    $subscriptionId="<subscription-id>"
    ```

1. Create a new JSON file named *capabilities.json* by using the capabilities manifest.

    ```json
    {
      "properties": {
        "enableMaterializedViews": true
      }
    }
    ```

> [!NOTE]
> The property name to enable the feature is `enableMaterializedViews`, which is the prior name. Enabling materialized views will enable global secondary indexes. 

1. Get the identifier of the account and store it in a shell variable named `$accountId`.

    ```azurecli
    $accountId="/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.DocumentDB/databaseAccounts/$accountName"
    ```

1. Enable the preview global secondary index feature for the account by using the REST API and [az rest](/cli/azure/reference-index#az-rest) with an HTTP `PATCH` verb.

    ```azurecli
    az rest \
        --method PATCH \
        --uri "https://management.azure.com/$accountId/?api-version=2022-11-15-preview" \
        --body @capabilities.json
    ```

---

> [!WARNING]
> The global secondary index feature can't be disabled on an account once enabled, however the global secondary builder and index containers themselves can be deprovisioned.

## Create a global secondary index builder

After the global secondary index feature is enabled for your account, you'll see a new page in the **Settings** section of the Azure portal for **Materialized Views Builder**. This is the same as the Global Secondary Index Builder, and uses a prior name for the same feature. You must provision a builder before creating index containers in your account. The builder is responsible for automatically hydrating data in the index containers and keeping them in sync with source containers. Learn more about options for [provisioning the global secondary index builder](./global-secondary-indexes.md#provisioning-the-global-secondary-index-builder).

### [Azure portal](#tab/azure-portal)

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Go to your Azure Cosmos DB for NoSQL account.

1. In the resource menu, select **Materialized Views Builder**.

1. On the **Materialized Views Builder** page, configure the SKU and the number of instances for the builder.

   > [!NOTE]
   > This resource menu option and page appear only when the global secondary index feature is enabled for the account.

1. Select **Save**.

### [Azure CLI](#tab/azure-cli)

1. Define the variables for the resource group and account name of your existing Azure Cosmos DB for NoSQL account.

    ```azurecli
    # Variable for resource group name
    $resourceGroupName="<resource-group-name>"
    
    # Variable for account name
    $accountName="<account-name>"
    
    # Variable for Azure subscription
    $subscriptionId="<subscription-id>"
    ```

1. Create a new JSON file named *builder.json* by using the builder manifest. Update the `instanceCount` and `instanceSize` as needed.

    ```json
    {
      "properties": {
        "serviceType": "materializedViewsBuilder",
        "instanceCount": 1,
        "instanceSize": "Cosmos.D4s"
      }
    }
    ```

> [!NOTE]
> The service type is `materializedViewsBuilder`, which is the prior name. Creating this resource will provision a global secondary index builder. 

1. Get the identifier of the account and store it in a shell variable named `$accountId`.

    ```azurecli
    $accountId="/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.DocumentDB/databaseAccounts/$accountName"
    ```

1. Enable the global secondary index builder for the account using the REST API and `az rest` with an HTTP `PUT` verb:

    ```azurecli
    az rest \
        --method PUT \
        --uri "https://management.azure.com$accountId/services/materializedViewsBuilder/?api-version=2022-11-15-preview" \
        --body @builder.json
    ```

1. Wait for a couple of minutes, and then check the status by using `az rest` again with the HTTP `GET` verb. The status in the output should now be `Running`.

    ```azurecli
    az rest \
        --method GET \
        --uri "https://management.azure.com$accountId/services/materializedViewsBuilder/?api-version=2022-11-15-preview"
    ```

---

## Create a global secondary index

After the feature is enabled and the global secondary index builder is provisioned, you can create index containers using the REST API.

1. Use the Azure portal, the Azure SDKs, the Azure CLI, or the REST API to create a source container that has `/customerId` as the partition key path. Name this source container `gsi-src`.

   > [!NOTE]
   > The `/customerId` field is used only as an example in this article. For your own containers, select a partition key that works for your solution.

1. Insert a few items in the source container. To follow the examples that are shown in this article, make sure that the items have `customerId` and `emailAddress` fields. A sample item might look like this:

    ```json
    {
      "id": "eaf0338e-2b61-4163-822f-7bef75bf51de",
      "customerId": "36c7cc3d-1709-45c6-819f-10e5586a6cb7",
      "emailAddress": "justine@contoso.com",
      "name": "Justine"
    }
    ```

   > [!NOTE]
   > In this example, you populate the source container with sample data before adding an index container. You can also create a global secondary index from an empty source container.

1. Now, create a global secondary index named `gsi-target` with a partition key path that is different from the source container. For this example, specify `/emailAddress` as the partition key path for the `gsi-target` container.

    1. Create a definition manifest for a global secondary index and save it in a JSON file named *gsi-definition.json*:

        ```json
        {
          "location": "North Central US",
          "tags": {},
          "properties": {
            "resource": {
              "id": "gsi-target",
              "partitionKey": {
                "paths": [
                  "/emailAddress"
                ]
              },
              "materializedViewDefinition": {
                "sourceCollectionId": "gsi-src",
                "definition": "SELECT c.customerId, c.emailAddress FROM c"
              }
            },
            "options": {
              "throughput": 400
            }
          }
        }        
        ```

   > [!IMPORTANT]
   > In the template, the property for defining global secondary indexes is `materializedViewDefinition`, which is the prior name.
   >
   > Notice that the partition key path is set as `/emailAddress`. The `sourceCollectionId` defines the source container for the index container and the `definition` contains a query to determine the data model. The global secondary index source container and definition query can't be changed once created. Learn more about [defining global secondary indexes](global-secondary-indexes.md#defining-global-secondary-indexes) and the query constraints.

1. Next, make a REST API call to create the global secondary index as defined in the *gsi-definition.json* file. Use the Azure CLI to make the REST API call.

    1. Create a variable for the name of the global secondary index and source database name:

        ```azurecli
        # This should match the resource ID you defined in your json file
        $gsiContainerName = "gsi-target"
        
        # Database name for the source and index containers
        $databaseName = "<Database that contains source container>"

        # Azure Cosmos DB account name
        $accountName = "<Azure Cosmos DB account name>"

        # Resource name for your Azure Cosmos DB account
        $resourceGroupName = "<Resource group for Azure Cosmos DB account>"

        # Subscription id for your Azure Cosmos DB account
        $subscriptionId = "<Subscription id>"
        ```

    1. Construct the resource ID using these variables.

        ```azurecli
        $accountId = "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.DocumentDB/databaseAccounts/$accountName"
        ```

    1. Make a REST API call to create the global secondary index:

        ```azurecli
        az rest \
            --method PUT \
            --uri "https://management.azure.com$accountId/sqlDatabases/ \
                  $databaseName/containers/$gsiContainerName/?api-version=2022-11-15-preview" \
            --body @gsi-definition.json \
            --headers content-type=application/json
        ```

    1. Check the status of the global secondary index container creation by using the REST API:

        ```azurecli
        az rest \
            --method GET \
            --uri "https://management.azure.com$accountId/sqlDatabases/
                  $databaseName/containers/$gsiContainerName/?api-version=2022-11-15-preview" \
            --headers content-type=application/json \
            --query "{mvCreateStatus: properties.Status}"
        ```

1. After the global secondary index is created, the builder automatically syncs changes with the source container. Try executing create, update, and delete operations in the source container. You'll see the same changes propagated to the index container.

## Query data from global secondary indexes

In this example, we have a source container partitioned on `customerId` and an index container partitioned on `emailAddress`. Without the index container, queries that only include the `emailAddress` would be cross-partition, but now they can use be executed against the global secondary index instead to increase efficiency. 

Querying data from global secondary indexes is similar to querying data from any other container. You can use the Azure portal, Azure SDKs, or REST API to query data in global secondary indexes.

### [.NET](#tab/dotnet)

```csharp
Container container = client.GetDatabase("gsi-db").GetContainer("gsi-target");

FeedIterator<MyClass> myQuery = container.GetItemQueryIterator<MyClass>(new QueryDefinition("SELECT * FROM c WHERE c.emailAddress = 'justine@contoso.com'"));
```

### [Java](#tab/java)

```java
CosmosAsyncDatabase container = client.getDatabase("gsi-db");
CosmosAsyncContainer container = database.getContainer("gsi-target");

CosmosPagedFlux<MyClass> pagedFluxResponse = container.queryItems(
        "SELECT * FROM c WHERE c.emailAddress = 'justine@contoso.com'", null, MyClass.class);
```

### [Node.js](#tab/nodejs)

```javascript
const database = client.database("gsi-db");
const container = database.container("gsi-target");

const querySpec = {
    query: "SELECT * FROM c WHERE c.emailAddress = 'justine@contoso.com'"
 };
const { resources: items } = await container.items
    .query(querySpec)
    .fetchAll();
```

### [Python](#tab/python)

```python
database = client.get_database_client("gsi-db")
container = database.get_container_client("gsi-target")

query = "SELECT * FROM c WHERE c.emailAddress = 'justine@contoso.com'"
container.query_items(
    query=query
)
```

---

## Next steps

> [!div class="nextstepaction"]
> [Data modeling and partitioning](model-partition-example.md)
> [Global secondary index overview](global-secondary-indexes.md)
