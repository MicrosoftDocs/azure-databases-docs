---
title: How to configure global secondary indexes (preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to configure global secondary indexes and use them to avoid expensive cross-partition queries.
author: jcocchi
ms.author: jucocchi
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 4/29/2025
ms.custom:
  - build-2025
---

# How to configure Azure Cosmos DB for NoSQL global secondary indexes (preview)

[!INCLUDE[NoSQL](includes/appliesto-nosql.md)]

> [!IMPORTANT]
> Azure Cosmos DB for NoSQL global secondary indexes are currently in preview. This preview is provided without a service-level agreement. At this time, we don't recommend that you use global secondary indexes for production workloads. Certain features of this preview might not be supported or might have constrained capabilities. For more information, see the [supplemental terms of use for Microsoft Azure previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Global secondary indexes provide a powerful way to optimize query performance and simplify application logic by storing your data with a different partition key and/ or data model. This article describes how to create global secondary indexes and how to use them to avoid cross-partition queries.

## Prerequisites

- An existing Azure Cosmos DB account.
  - If you have an Azure subscription, [create a new account](how-to-create-account.md?tabs=azure-portal).
  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Enable global secondary indexes

Enable the global secondary index feature for your Azure Cosmos DB account. [Continuous backups](continuous-backup-restore-introduction.md) must be turned on for the account before enabling global secondary indexes.

### [Azure portal](#tab/azure-portal)

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Go to your Azure Cosmos DB for NoSQL account.

1. In the resource menu, select **Settings**.

1. Navigate to the **Features** page. Then select **Global Secondary Index for NoSQL API (preview)** and **Enable**.

    :::image type="content" source="./media/how-to-configure-global-secondary-indexes/enable-global-secondary-indexes.png" alt-text="Screenshot of how to enable the Global Secondary Index feature in the Azure portal." :::

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
    > The property name to enable global secondary indexes is `enableMaterializedViews`, which is the former feature name. Enabling materialized views will enable global secondary indexes. 

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

## Create a global secondary index

After the global secondary index feature is enabled, you can create global secondary indexes.

### Create a source container

Global secondary indexes store a copy of data from the source container. Before creating a global secondary index, create the source container that your index container will be built from. If you already have a container in your Azure Cosmos DB account that you would like to use as the source, you can skip these steps.

1. Use the Azure portal, the Azure SDKs, the Azure CLI, or the REST API to create a source container named `gsi-src` with `/customerId` as the partition key path.

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

   > [!TIP]
   > In this example, you populate the source container with sample data before adding an index container. You can also create a global secondary index from an empty source container.

### Create a global secondary index container

Once the source container is created, you can create a global secondary index container using the Azure portal or Azure CLI.

### [Azure portal](#tab/azure-portal)

1. Navigate to **Data Explorer** in your Azure Cosmos DB account. Select your source container, `gsi-src` in this example, and select **New Global Secondary Index** from the drop-down.

    :::image type="content" source="./media/how-to-configure-global-secondary-indexes/create-global-secondary-indexes.png" alt-text="Screenshot of how to create a Global Secondary Index in the Data Explorer page of the Azure portal." :::

1. The source container ID will be populated for you. In the **Index container id** field, enter `gsi-target`.

1. In the **Global secondary index definition** field, enter `SELECT c.customerId, c.emailAddress FROM c`.

1. In the **Partition key** field, enter `/emailAddress`.

    :::image type="content" source="./media/how-to-configure-global-secondary-indexes/configure-global-secondary-indexes.png" alt-text="Screenshot of how to configure a Global Secondary Index in the Data Explorer page of the Azure portal." :::

1. Global secondary index containers must use autoscale throughput. Configure any other container settings you'd like and select **OK** to create the global secondary index container.

1. After the global secondary index container is created, data is automatically synced from the source container. Try executing create, update, and delete operations in the source container. You'll see the same changes propagated to items in the global secondary index.

### [Azure CLI](#tab/azure-cli)

1. Create a global secondary index named `gsi-target` with a partition key path that is different from the source container. For this example, specify `/emailAddress` as the partition key path for the `gsi-target` container.

    1. Create a definition manifest for a global secondary index and save it in a JSON file named *gsi-definition.json*. Global secondary index containers must use autoscale throughput. At this stage, you can also define any other relevant container properties such as an indexing policy.

        ```json
        {
          "location": "West US 2",
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
              "autoscaleSettings": {
                "maxThroughput": 1000
              }
            }
          }
        }        
        ```

   > [!IMPORTANT]
   > Notice that the partition key path is set as `/emailAddress`.
   >
   > The property for defining global secondary indexes is `materializedViewDefinition`, which is the former name for this feature. The `sourceCollectionId` defines the source container and the `definition` contains a query to determine the data model of the index container. The global secondary index source container and definition query can't be changed once created. Learn more about [defining global secondary indexes](global-secondary-indexes.md#defining-global-secondary-indexes) and the query constraints.

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
            --uri "https://management.azure.com$accountId/sqlDatabases/$databaseName/containers/$gsiContainerName/?api-version=2022-11-15-preview" \
            --body @gsi-definition.json \
            --headers content-type=application/json \
            --output json \
            --verbose
        ```

    1. Check the status of the global secondary index container creation by using the REST API:

        ```azurecli
        az rest \
            --method GET \
            --uri "https://management.azure.com$accountId/sqlDatabases/$databaseName/containers/$gsiContainerName/?api-version=2022-11-15-preview" \
            --headers content-type=application/json \
            --query "{mvCreateStatus: properties.Status}"
        ```

1. After the global secondary index is created, data is automatically synced from the source container. Try executing create, update, and delete operations in the source container. You'll see the same changes propagated to items in the global secondary index.

---

## Query data from global secondary indexes

In this example, we have a source container partitioned on `customerId` and a global secondary index container partitioned on `emailAddress`. Without the index container, queries that only include the `emailAddress` would be cross-partition, but now they can be run against the global secondary index instead to increase efficiency.

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

### [Go](#tab/go)

```go
gsiContainer, err := client.NewContainer("gsi-db", "gsi-target")

pager := gsiContainer.NewQueryItemsPager("select * from c where c.state = @state", azcosmos.NewPartitionKey(), &azcosmos.QueryOptions{
	QueryParameters: []azcosmos.QueryParameter{
		{
			Name:  "@state",
			Value: "Alaska",
		},
	},
})

if pager.More() {
  // Iterate through the results
  // page, _ := pager.NextPage(context.Background())
}
```


---

## Next steps

> [!div class="nextstepaction"]
> [Data modeling and partitioning](model-partition-example.md)
> [Global secondary index overview](global-secondary-indexes.md)
