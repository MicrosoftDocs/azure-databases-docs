---
title: How to configure materialized views (preview)
titleSuffix: Azure Cosmos DB for NoSQL
description: Learn how to configure materialized views and use them to avoid expensive cross-partition queries.
author: jcocchi
ms.author: jucocchi
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 3/4/2025
---

# How to configure Azure Cosmos DB for NoSQL materialized views (preview)

[!INCLUDE[NoSQL](../includes/appliesto-nosql.md)]

> [!IMPORTANT]
> Azure Cosmos DB for NoSQL materialized views are currently in preview. You can enable this feature by using the Azure portal and the feature can't be disabled. This preview is provided without a service-level agreement. At this time, we don't recommend that you use materialized views for production workloads. Certain features of this preview might not be supported or might have constrained capabilities. For more information, see the [supplemental terms of use for Microsoft Azure previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Materialized views provide a powerful way to optimize query performance and simplify application logic by creating views of your data with a different partition key and/ or data model. This article describes how to create materialized views and how to use them to handle cross-partition queries efficiently.

## Prerequisites

- An existing Azure Cosmos DB account.
  - If you have an Azure subscription, [create a new account](how-to-create-account.md?tabs=azure-portal).
  - If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.
  - Alternatively, you can [try Azure Cosmos DB free](../try-free.md) before you commit.

## Enable materialized views

The materialized views feature needs to be enabled for your Azure Cosmos DB account before provisioning a builder or creating views.

### [Azure portal](#tab/azure-portal)

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Go to your Azure Cosmos DB for NoSQL account.

1. In the resource menu, select **Settings**.

1. In the **Features** section under **Settings**, toggle the **Materialized View for NoSQL API (preview)** option to **On**.

1. In the new dialog, select **Enable** to enable this feature for the account.

### [Azure CLI](#tab/azure-cli)

Use the Azure CLI to enable the materialized views feature either by using a native command or a REST API operation on your Azure Cosmos DB for NoSQL account.

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

1. Get the identifier of the account and store it in a shell variable named `$accountId`.

    ```azurecli
    $accountId="/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.DocumentDB/databaseAccounts/$accountName"
    ```

1. Enable the preview materialized views feature for the account by using the REST API and [az rest](/cli/azure/reference-index#az-rest) with an HTTP `PATCH` verb.

    ```azurecli
    az rest \
        --method PATCH \
        --uri "https://management.azure.com/$accountId/?api-version=2022-11-15-preview" \
        --body @capabilities.json
    ```

---

> [!WARNING]
> The materialized views feature can't be disabled on an account once enabled, however the materialized views builder and views themselves can be deprovisioned.

## Create a materialized view builder

After the materialized views feature is enabled for your account, you'll see a new page in the **Settings** section of the Azure portal for **Materialized Views Builder**. You must provision a materialized views builder before creating views in your account. The builder is responsible for automatically hydrating data in the views and keeping them in sync with source containers. Learn more about options for [provisioning the materialized view builder](./materialized-views.md#provisioning-the-materialized-views-builder).

### [Azure portal](#tab/azure-portal)

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Go to your Azure Cosmos DB for NoSQL account.

1. In the resource menu, select **Materialized Views Builder**.

1. On the **Materialized Views Builder** page, configure the SKU and the number of instances for the builder.

   > [!NOTE]
   > This resource menu option and page appear only when the materialized views feature is enabled for the account.

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

1. Get the identifier of the account and store it in a shell variable named `$accountId`.

    ```azurecli
    $accountId="/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.DocumentDB/databaseAccounts/$accountName"
    ```

1. Enable the materialized views builder for the account using the REST API and `az rest` with an HTTP `PUT` verb:

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

## Create a materialized view

After the feature is enabled and the materialized view builder is provisioned, you can create materialized views using the REST API.

1. Use the Azure portal, the Azure SDKs, the Azure CLI, or the REST API to create a source container that has `/customerId` as the partition key path. Name this source container `mv-src`.

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
   > In this example, you populate the source container with sample data before adding a view. You can also create a materialized view from an empty source container.

1. Now, create a materialized view named `mv-target` with a partition key path that is different from the source container. For this example, specify `/emailAddress` as the partition key path for the `mv-target` container.

    1. Create a definition manifest for a materialized view and save it in a JSON file named *mv-definition.json*:

        ```json
        {
          "location": "North Central US",
          "tags": {},
          "properties": {
            "resource": {
              "id": "mv-target",
              "partitionKey": {
                "paths": [
                  "/emailAddress"
                ]
              },
              "materializedViewDefinition": {
                "sourceCollectionId": "mv-src",
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
   > In the template, notice that the partition key path is set as `/emailAddress`. The `sourceCollectionId` defines the source container for the view and the `definition` contains a query to determine the data model of the view. Learn more about [defining materialized views](materialized-views.md#defining-materialized-views) and the query constraints.
   >
   > The materialized view source container and definition query can't be changed once created.

1. Next, make a REST API call to create the materialized view as defined in the *mv-definition.json* file. Use the Azure CLI to make the REST API call.

    1. Create a variable for the name of the materialized view and source database name:

        ```azurecli
        # This should match the resource ID you defined in your json file
        $materializedViewName = "mv-target"
        
        # Database name for the source and view containers
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

    1. Make a REST API call to create the materialized view:

        ```azurecli
        az rest \
            --method PUT \
            --uri "https://management.azure.com$accountId/sqlDatabases/ \
                  $databaseName/containers/$materializedViewName/?api-version=2022-11-15-preview" \
            --body @mv-definition.json \
            --headers content-type=application/json
        ```

    1. Check the status of the materialized view container creation by using the REST API:

        ```azurecli
        az rest \
            --method GET \
            --uri "https://management.azure.com$accountId/sqlDatabases/
                  $databaseName/containers/$materializedViewName/?api-version=2022-11-15-preview" \
            --headers content-type=application/json \
            --query "{mvCreateStatus: properties.Status}"
        ```

1. After the materialized view is created, the materialized view builder automatically syncs changes with the source container. Try executing create, update, and delete operations in the source container. You'll see the same changes propagated to the materialized view container.

## Query data from materialized views

In this example, we have a source container partitioned on `customerId` and a view partitioned on `emailAddress`. Without the view, queries that only include the `emailAddress` would be cross-partition, but now they can use be executed against the view instead to increase efficiency. 

Querying data from materialized views is similar to querying data from any other container. You can use the Azure portal, Azure SDKs, or REST API to query data in materialized views.

### [.NET](#tab/dotnet)

```csharp
Container container = client.GetDatabase("mv-db").GetContainer("mv-target");

FeedIterator<MyClass> myQuery = container.GetItemQueryIterator<MyClass>(new QueryDefinition("SELECT * FROM c WHERE c.emailAddress = 'justine@contoso.com'"));
```

### [Java](#tab/java)

```java
CosmosAsyncDatabase container = client.getDatabase("mv-db");
CosmosAsyncContainer container = database.getContainer("mv-target");

CosmosPagedFlux<MyClass> pagedFluxResponse = container.queryItems(
        "SELECT * FROM c WHERE c.emailAddress = 'justine@contoso.com'", null, MyClass.class);
```

### [Node.js](#tab/nodejs)

```javascript
const database = client.database("mv-db");
const container = database.container("mv-target");

const querySpec = {
    query: "SELECT * FROM c WHERE c.emailAddress = 'justine@contoso.com'"
 };
const { resources: items } = await container.items
    .query(querySpec)
    .fetchAll();
```

### [Python](#tab/python)

```python
database = client.get_database_client("mv-db")
container = database.get_container_client("mv-target")

query = "SELECT * FROM c WHERE c.emailAddress = 'justine@contoso.com'"
container.query_items(
    query=query
)
```

---

## Next steps

> [!div class="nextstepaction"]
> [Data modeling and partitioning](model-partition-example.md)
> [Materialized views overview](materialized-views.md)
