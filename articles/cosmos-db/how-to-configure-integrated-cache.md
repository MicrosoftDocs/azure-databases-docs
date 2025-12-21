---
title: How to Configure the Integrated Cache
description: Learn how to configure the Azure Cosmos DB integrated cache
author: jcocchi
ms.service: azure-cosmos-db
ms.subservice: nosql
ms.topic: how-to
ms.date: 10/08/2024
ms.author: jucocchi
ms.custom: sfi-image-nochange
appliesto:
  - ✅ NoSQL
---

# How to configure the Azure Cosmos DB integrated cache

This article describes how to provision a dedicated gateway, configure the integrated cache, and connect your application. 

## Prerequisites

- If you don't have an [Azure subscription](/azure/guides/developer/azure-developer-guide#understanding-accounts-subscriptions-and-billing), create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
- An existing application that uses Azure Cosmos DB. If you don't have one, [here are some examples](https://github.com/AzureCosmosDB/labs).
- An existing [Azure Cosmos DB API for NoSQL account](quickstart-portal.md).

## Provision the dedicated gateway

1. Navigate to an Azure Cosmos DB account in the Azure portal and select the **Dedicated Gateway** tab.

   :::image type="content" source="./media/how-to-configure-integrated-cache/dedicated-gateway-tab.png" alt-text="Screenshot of the Azure portal that shows how to navigate to the Azure Cosmos DB dedicated gateway tab." lightbox="./media/how-to-configure-integrated-cache/dedicated-gateway-tab.png" :::

2. Fill out the **Dedicated gateway** form with the following details:

   * **Dedicated Gateway** - Turn on the  toggle to **Provisioned**. 
   * **SKU** - Select a SKU with the required compute and memory size. The integrated cache will use approximately 50% of the memory, and the remaining memory is used for metadata and routing requests to the backend partitions.
   *  **Number of instances** - Number of nodes. For development purpose, we recommend starting with one node of the D4 size. Based on the amount of data you need to cache and to achieve high availability, you can increase the node size after initial testing.

   :::image type="content" source="./media/how-to-configure-integrated-cache/dedicated-gateway-input.png" alt-text="Screenshot of the Azure portal dedicated gateway tab that shows sample input settings for creating a dedicated gateway cluster." lightbox="./media/how-to-configure-integrated-cache/dedicated-gateway-input.png" :::

3. Select **Save** and wait about 5-10 minutes for the dedicated gateway provisioning to complete. When the provisioning is done, you'll see the following notification:

   :::image type="content" source="./media/how-to-configure-integrated-cache/dedicated-gateway-notification.png" alt-text="Screenshot of a notification in the Azure portal that shows how to check if dedicated gateway provisioning is complete." lightbox="./media/how-to-configure-integrated-cache/dedicated-gateway-notification.png" :::

## Configure your application to use the integrated cache

When you provision a dedicated gateway, an integrated cache is automatically created. You don’t need to connect all applications using Azure Cosmos DB to the dedicated gateway if they don't need to use the integrated cache. Adding a dedicated gateway doesn't impact the existing ways of connecting to Azure Cosmos DB. For example, you could have one `CosmosClient` connect using gateway mode and the dedicated gateway endpoint while another `CosmosClient` uses direct mode. 

### Authenticate with role-based access control

The dedicated gateway uses the same permissions, role definitions and role assignments as Azure Cosmos DB. If you already have role-based access control (RBAC) configured for data plane operations in your Azure Cosmos DB account, you can also use it for authenticating to the dedicated gateway. Learn about [RBAC for Azure Cosmos DB data plane](how-to-connect-role-based-access-control.md#grant-data-plane-role-based-access) operations.

Configure your `CosmosClient` by setting the dedicated gateway endpoint, credential, and configuring [gateway connectivity mode](sdk-connection-modes.md#available-connectivity-modes). All dedicated gateway endpoints follow the same pattern. Remove `documents.azure.com` from your original endpoint and replace it with `sqlx.cosmos.azure.com`. A dedicated gateway will always have the same endpoint, even if you remove and reprovision it.

### [.NET](#tab/dotnet)

```csharp
using Azure.Core;
using Azure.Identity;
using Microsoft.Azure.Cosmos;

string endpoint = "<dedicated-gateway-endpoint>";

TokenCredential credential = new DefaultAzureCredential();

CosmosClient client = new(endpoint, credential, new CosmosClientOptions { ConnectionMode = ConnectionMode.Gateway });
```

> [!IMPORTANT]
> Direct connectivity mode is the default in the .NET SDK. You must explicitly configure gateway mode to use the dedicated gateway.

### [Java](#tab/java)

```java
import com.azure.cosmos.CosmosClient;
import com.azure.cosmos.CosmosClientBuilder;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;

public class NoSQL{
    public static void main(String[] args){
        DefaultAzureCredential credential = new DefaultAzureCredentialBuilder()
            .build();
        
        CosmosClient client = new CosmosClientBuilder()
            .endpoint("<dedicated-gateway-endpoint>")
            .gatewayMode()
            .credential(credential);
            .buildClient();
    }
}
```

> [!IMPORTANT]
> Direct connectivity mode is the default in the Java SDK. You must explicitly configure gateway mode to use the dedicated gateway.

### [Node.js](#tab/nodejs)

```javascript
const { CosmosClient } = require('@azure/cosmos');
const { DefaultAzureCredential } = require('@azure/identity');

const endpoint = '<dedicated-gateway-endpoint>';

const credential = new DefaultAzureCredential();

const client = new CosmosClient({ endpoint, aadCredentials:credential})
```

### [Python](#tab/python)

```python
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

endpoint = "<dedicated-gateway-endpoint>"

credential = DefaultAzureCredential()

client = CosmosClient(endpoint, credential=credential)
```

### [Go](#tab/go)

```go
endpoint = "<dedicated-gateway-endpoint>"
client, _ := azcosmos.NewClient(endpoint, creds, nil)
```

---

### Authenticate with connection strings

1.	Modify your application's connection string to use the new dedicated gateway endpoint.

      The updated dedicated gateway connection string is in the **Keys** blade:
   
      :::image type="content" source="./media/how-to-configure-integrated-cache/dedicated-gateway-connection-string.png" alt-text="Screenshot of the Azure portal keys tab with the dedicated gateway connection string." lightbox="./media/how-to-configure-integrated-cache/dedicated-gateway-connection-string.png" :::

      All dedicated gateway connection strings follow the same pattern. Remove `documents.azure.com` from your original connection string and replace it with `sqlx.cosmos.azure.com`. A dedicated gateway will always have the same connection string, even if you remove and reprovision it.

2. If you're using the .NET or Java SDK, set the connection mode to [gateway mode](sdk-connection-modes.md#available-connectivity-modes). This step isn't necessary for the Python and Node.js SDKs since they don't have additional options of connecting besides gateway mode.

> [!IMPORTANT]
> If you are using the latest .NET or Java SDK version, the default connection mode is direct mode. In order to use the integrated cache, you must override this default.

## Adjust request consistency

You must ensure the request consistency is session or eventual. If not, the request will always bypass the integrated cache. The easiest way to configure a specific consistency for all read operations is to [set it at the account-level](consistency-levels.md#configure-the-default-consistency-level). You can also configure consistency at the [request-level](how-to-manage-consistency.md#override-the-default-consistency-level), which is recommended if you only want a subset of your reads to utilize the integrated cache.

## Adjust MaxIntegratedCacheStaleness

Configure `MaxIntegratedCacheStaleness`, which is the maximum time in which you're willing to tolerate stale cached data. It's recommended to set the `MaxIntegratedCacheStaleness` as high as possible because it will increase the likelihood that repeated point reads and queries can be cache hits. If you set `MaxIntegratedCacheStaleness` to 0, your read request will **never** use the integrated cache, regardless of the consistency level. When not configured, the default `MaxIntegratedCacheStaleness` is 5 minutes.

>[!NOTE]
> The `MaxIntegratedCacheStaleness` can be set as high as 10 years. In practice, this value is the maximum staleness and the cache may be reset sooner due to node restarts which may occur. 

Adjusting the `MaxIntegratedCacheStaleness` is supported in these versions of each SDK:

| SDK | Supported versions |
| --- | ------------------ |
| **.NET SDK v3** | *>= 3.30.0* |
| **Java SDK v4** | *>= 4.34.0* |
| **Node.js SDK** | *>=3.17.0* |
| **Python SDK**  | *>=4.3.1* |
| **Go SDK**      | *>=1.1.0* |

### [.NET](#tab/dotnet)

```csharp
FeedIterator<MyClass> myQuery = container.GetItemQueryIterator<MyClass>(new QueryDefinition("SELECT * FROM c"), requestOptions: new QueryRequestOptions
        {
            DedicatedGatewayRequestOptions = new DedicatedGatewayRequestOptions 
            { 
                MaxIntegratedCacheStaleness = TimeSpan.FromMinutes(30) 
            }
        }
);
```

### [Java](#tab/java)

```java
DedicatedGatewayRequestOptions dgOptions = new DedicatedGatewayRequestOptions()
   .setMaxIntegratedCacheStaleness(Duration.ofMinutes(30));
CosmosQueryRequestOptions queryOptions = new CosmosQueryRequestOptions()
   .setDedicatedGatewayRequestOptions(dgOptions);

CosmosPagedFlux<MyClass> pagedFluxResponse = container.queryItems(
        "SELECT * FROM c", queryOptions, MyClass.class);
```

### [Node.js](#tab/nodejs)

```javascript
 const queryRequestOptions = {
   maxIntegratedCacheStalenessInMs: 1800000 };
 const querySpec = {
   query: "SELECT * from c"
 };
 const { resources: items } = await container.items
   .query(querySpec, queryRequestOptions)
   .fetchAll();
```

### [Python](#tab/python)

```python
query = "SELECT * FROM c"
container.query_items(
    query=query,
    max_integrated_cache_staleness_in_ms=1800000
)
```

### [Go](#tab/go)

```go
staleness := 18000 * time.Millisecond

container.NewQueryItemsPager("select * from c", azcosmos.NewPartitionKey(), &azcosmos.QueryOptions{
	DedicatedGatewayRequestOptions: &azcosmos.DedicatedGatewayRequestOptions{
		MaxIntegratedCacheStaleness: &staleness,
	},
})
```

---

## Bypass the integrated cache

Use the `BypassIntegratedCache` request option to control which requests use the integrated cache. Writes, point reads, and queries that bypass the integrated cache won't use cache storage, saving space for other items. Requests that bypass the cache are still routed through the dedicated gateway. These requests are served from the backend and cost RUs.

Bypassing the cache is supported in these versions of each SDK:

| SDK | Supported versions |
| --- | ------------------ |
| **.NET SDK v3** | *>= 3.39.0* |
| **Java SDK v4** | *>= 4.49.0* |
| **Node.js SDK** | *>= 4.1.0* |
| **Python SDK**  | Not supported |

### [.NET](#tab/dotnet)

```csharp
FeedIterator<MyClass> myQuery = container.GetItemQueryIterator<MyClass>(new QueryDefinition("SELECT * FROM c"), requestOptions: new QueryRequestOptions
        {
            DedicatedGatewayRequestOptions = new DedicatedGatewayRequestOptions 
            { 
                BypassIntegratedCache = true
            }
        }
);
```

### [Java](#tab/java)

```java
DedicatedGatewayRequestOptions dgOptions = new DedicatedGatewayRequestOptions()
   .setIntegratedCacheBypassed(true);
CosmosQueryRequestOptions queryOptions = new CosmosQueryRequestOptions()
   .setDedicatedGatewayRequestOptions(dgOptions);

CosmosPagedFlux<MyClass> pagedFluxResponse = container.queryItems(
        "SELECT * FROM c", queryOptions, MyClass.class);
```

### [Node.js](#tab/nodejs)

```javascript
    const queryRequestOptions = {
      bypassIntegratedCache: true };
    const querySpec = {
      query: "SELECT * from c"
    };
    const { resources: items, requestCharge: queryCharge } = await container.items
      .query(querySpec, queryRequestOptions)
      .fetchAll();
```

### [Python](#tab/python)

The bypass integrated cache request option isn't available in the Python SDK.

### [Go](#tab/go)

The bypass integrated cache request option isn't available in the Go SDK.

---

## Verify cache hits

Finally, you can restart your application and verify integrated cache hits for repeated point reads or queries by seeing if the request charge is 0. Once you’ve modified your `CosmosClient` to use the dedicated gateway endpoint, all requests will be routed through the dedicated gateway.

For a read request (point read or query) to utilize the integrated cache, **all** of the following criteria must be true:

-	Your client connects to the dedicated gateway endpoint
-  Your client uses gateway mode (Python and Node.js SDKs always use gateway mode)
-	The consistency for the request must be set to session or eventual

> [!NOTE]
> Do you have any feedback about the integrated cache? We want to hear it! Feel free to share feedback directly with the Azure Cosmos DB engineering team:
cosmoscachefeedback@microsoft.com


## Next steps

- [Integrated cache FAQ](integrated-cache-faq.md)
- [Integrated cache overview](integrated-cache.md)
- [Dedicated gateway](dedicated-gateway.md)
